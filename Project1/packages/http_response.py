import datetime

from packages.http_params import HttpMessageHeader, HttpContentType, get_header


class HttpResponse:
    http_version = None
    status_code = None
    reason_message = None

    content_type = None
    content_length = None

    location = None

    host = None
    body = None

    def construct_from_string(self, message: str):
        lines = message.split('\r\n')

        # Initializing method information
        response_line = lines[0]
        self.http_version = response_line.split(' ')[0]
        self.status_code = int(response_line.split(' ')[1])
        self.reason_message = response_line.split(' ')[2]

        body_started = False
        body = ''

        for line in lines:
            if body_started:
                body += line + '\n'
            else:
                if line == '':
                    body_started = True
                else:
                    header = get_header(line)
                    if header.key == "Content-Type":
                        print(header.value)
                        content_type = HttpContentType.unknown
                        try:
                            self.content_type = content_type.from_str(header.value.split(';')[0].strip())
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
                    # elif header.key == "Date":
                    #     self.date = datetime.datetime.strptime(header.value[:-4], "%a, %d %b %Y %H:%M:%S")
                    #     print(self.date)
        if len(body) > 0:
            self.body = body[:-2]

    def __str__(self):
        return (self.http_version + " " + str(self.status_code) + " " + self.reason_message) + \
               (('\r\nHost: ' + self.host) if (self.host is not None) else "") + \
               (('\r\nLocation: ' + self.location) if (self.location is not None) else "") + \
               (('\r\nContent-Type: ' + self.content_type.value) if (self.content_type is not None) else "") + \
               (('\r\nContent-Length: ' + str(self.content_length)) if (self.content_length is not None) else "") + \
               (('\r\nDate: ' + self.date.strftime("%a, %d %b %Y %H:%M:%S") + " GMT") if (
                           self.date is not None) else "") + \
               (('\r\n\r\n' + self.body) if (self.body is not None) else "")

    def __init__(self, http_version: str = None, status_code: int = None, reason_message: str = None,
                 content_type: HttpContentType = None, content_length: int = None, date: datetime = None,
                 location: str = None,
                 host: str = None, body=None):
        self.http_version = http_version
        self.status_code = status_code
        self.reason_message = reason_message
        self.content_type = content_type
        self.content_length = content_length
        self.date = date
        self.location = location
        self.host = host
        self.body = body
