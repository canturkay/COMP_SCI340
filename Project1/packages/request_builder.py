from packages.http_params import HttpMessageHeader, get_header


class RequestBuilder:
    messages = {}


class UnFinishedRequest:
    message = None
    body_bytes = None
    content_length = None

    def receive_data(self, data):
        self.message += data
        lines = self.message.split(b'\r\n')
        if self.content_length is None:
            for line in lines:
                header = get_header(line)
                if header.key == "Content-Length":
                    try:
                        self.content_length = int(header.value)
                    except:
                        print("Could not parse content length from header:\n" + header.key + ":" + header.value)



    def __init__(self, message, body_bytes):
        self.message = message
        self.body_bytes = body_bytes
