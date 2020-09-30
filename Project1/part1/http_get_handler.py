import socket

from packages.http_params import HttpMethod, HttpContentType
from packages.http_request import HttpRequest
from packages.http_response import HttpResponse


class HttpHandler:
    sock = None

    def get(self, url: str, recursion_count: int = 0) -> HttpResponse:
        if len(url) < 7 or url[0:7] != "http://":
            return HttpResponse(
                None,
                400,
                "HTTPS is not available")

        if recursion_count >= 10:
            return HttpResponse(
                None,
                408,
                "Recursion limit of 10 exceeded")

        url_arr = url.split("/")
        base = url_arr[2]
        addr = "/".join(url_arr[3:])
        port = 80

        if base.find(':') != -1:
            split_base = base.split(':')
            base = split_base[0]
            port = int(split_base[1])

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((base, port))

        request = HttpRequest(
            http_method=HttpMethod.GET,
            address='/' + addr,
            http_version="HTTP/1.1",
            host=base,
        )

        self.sock.sendall(str(request).encode('ASCII'))
        body_length = None
        content_length = None
        response_raw = b''
        response = HttpResponse()

        while content_length is None or body_length is None or body_length < content_length:
            new_data = self.sock.recv(4096)

            if new_data is None or new_data == '':
                break

            response_raw += new_data

            response.construct_from_string(response_raw.decode('ASCII'))

            content_length = response.content_length
            body_length = len(response_raw.split(b'\r\n\r\n')[1])

        self.sock.close()
        response = HttpResponse()
        response.construct_from_string(response_raw.decode('ASCII'))

        if response.status_code == 301 or response.status_code == 302:
            if response.location is None:
                return HttpResponse(400, "Redirection failed, Location header not found")
            print("Redirecting to: " + response.location)
            return self.get(response.location, recursion_count=recursion_count + 1)

        if response.content_type is None:
            return HttpResponse(400, "Content-Type header not found")
        if response.content_type is not HttpContentType.html:
            return HttpResponse(400, "Content type is not text/html")
        return HttpResponse(status_code=response.status_code, reason_message=response.reason_message,
                            body=response.body)
