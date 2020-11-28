from packages.http_params import HttpMessageHeader, HttpMethod, HttpContentType, get_header


class HttpRequest:
    http_method = None
    address = None
    http_version = None

    content_type = None
    content_length = None

    host = None
    body = None

    def __str__(self):
        return (self.http_method.value + " " + self.address + " " + self.http_version) + \
               (('\r\nHost: ' + self.host) if (self.host is not None) else "") + \
               (('\r\nContent-Type: ' + self.content_type.value) if (self.content_type is not None) else "") + \
               (('\r\nContent-Length: ' + str(self.content_length)) if (self.content_length is not None) else "") + \
               '\r\n\r\n' + \
               (self.body + '\r\n\r\n' if (self.body is not None) else "")

    def construct_from_string(self, message: str):
        lines = message.split('\r\n')

        # Initializing method information
        method_line = lines[0]

        if ' ' not in method_line:
            return True

        http_method = HttpMethod.unknown
        try:
            self.http_method = http_method.from_str(method_line.split(' ')[0].strip())
        except:
            self.http_method = HttpMethod.unknown
        self.address = method_line.split(' ')[1]
        self.http_version = method_line.split(' ')[2]

        body_started = False
        body = ''
        for line in lines:
            if body_started:
                body += line + '\r\n'
            else:
                if line == '':
                    body_started = True
                else:
                    header = get_header(line)
                    if header.key == "Content-Type":
                        content_type = HttpContentType.unknown
                        try:
                            self.content_type = content_type.from_str(header.value)
                        except:
                            self.content_type = HttpContentType.unknown
                    elif header.key == "Content-Length":
                        try:
                            self.content_length = int(header.value)
                        except:
                            print("Could not parse content length from header:\n" + header.key + ":" + header.value)
                    elif header.key == "Host":
                        self.host = header.value
        if len(body) > 0:
            self.body = body[:-1]

    def __init__(self, http_method: HttpMethod = None, address: str = None, http_version: str = None,
                 content_type: HttpContentType = None, content_length: int = None,
                 host: str = None, body=None):
        self.http_method = http_method
        self.address = address
        self.http_version = http_version
        self.content_type = content_type
        self.content_length = content_length
        self.host = host
        self.body = body
