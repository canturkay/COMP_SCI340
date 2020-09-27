from packages.http_params import HttpMessageHeader, HttpMethod, HttpContentType


class HttpRequest:
    http_method = None
    address = None
    http_version = None

    content_type = None
    content_length = None

    location = None

    host = None
    body = None

    def __str__(self):
        return (self.http_method.value + " " + self.address + " " + self.http_version) + \
               (('\nHost: ' + self.host) if (self.host is not None) else "") + \
               (('\nLocation: ' + self.location) if (self.location is not None) else "") + \
               (('\nContent-Type: ' + self.content_type.value) if (self.content_type is not None) else "") + \
               (('\nContent-Length: ' + str(self.content_length)) if (self.content_length is not None) else "") + \
               (('\n\n' + self.body) if (self.body is not None) else "")

    def construct_from_string(self, message: str):
        lines = message.split('\r\n')

        # Initializing method information
        method_line = lines[0]
        try:
            self.http_method = HttpMethod[method_line.split(' ')[0]]
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
                    header = self.get_header(line)
                    if header.key == "Content-Type":
                        try:
                            self.content_type = HttpContentType[header.value]
                        except:
                            self.content_type = HttpContentType.unknown
                    elif header.key == "Content-Length":
                        try:
                            self.content_length = int(header.value)
                        except:
                            print("Could not parse content length from header:\n" + header.key + ":" + header.value)
                    elif header.key == "Location":
                        self.location = header.value
                    elif header.key == "Host":
                        self.host = header.value
        if len(body) > 0:
            self.body = body[:-1]

    @staticmethod
    def get_header(line: str) -> HttpMessageHeader:
        line_values = line.split(' ')
        if len(line_values) >= 2:
            header_key = line_values[0][:-1]
            header_value = ' '.join(line_values[1:])
            return HttpMessageHeader(header_key, header_value)
        else:
            return HttpMessageHeader(None, None)

    def __init__(self, http_method: HttpMethod = None, address: str = None, http_version: str = None,
                 content_type: HttpContentType = None, content_length: int = None, location: str = None,
                 host: str = None, body=None):
        self.http_method = http_method
        self.address = address,
        self.http_version = http_version
        self.content_type = content_type
        self.content_length = content_length
        self.location = location
        self.host = host
        self.body = body
