from packages.http_params import HttpMessageHeader, get_header


class RequestBuilder:
    messages = {}

    def receive_data(self, addr: str, data: str) -> str:
        if addr not in self.messages:
            self.messages[addr] = UnFinishedRequest()

        self.messages[addr].receive_data(data)
        if self.messages[addr].body_bytes is not None and\
                self.messages[addr].body_bytes == self.messages[addr].content_length:
            return self.messages[addr].message

        return None


class UnFinishedRequest:
    message = None
    body_bytes = None
    content_length = None

    def receive_data(self, data: str):
        if self.message is None:
            self.message = data
        else:
            self.message += data
        lines = self.message.split('\r\n')
        if self.content_length is None:
            for line in lines:
                header = get_header(line)
                if header.key == "Content-Length":
                    try:
                        self.content_length = int(header.value)
                    except:
                        print("Could not parse content length from header:\n" + header.key + ":" + header.value)

        if self.content_length is not None:
            parts = self.message.split('\r\n\r\n')
            if len(parts) > 1:
                self.body_bytes = len(parts[1])
