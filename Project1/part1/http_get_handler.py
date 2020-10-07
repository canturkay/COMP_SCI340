import socket
import sys

from packages.http_params import HttpMethod, HttpContentType
from packages.http_request import HttpRequest
from packages.http_response import HttpResponse


class HttpHandler:
    sock = None

    def get(self, url: str, recursion_count: int = 0) -> HttpResponse:
        if len(url) < 7 or url[0:7] != "http://":
            return HttpResponse(
                status_code=
                400,
                reason_message="HTTPS is not available")

        if recursion_count >= 10:
            return HttpResponse(
                status_code=408,
                reason_message="Recursion limit of 10 exceeded")

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
        self.sock.settimeout(3)

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

        while body_length is None or (content_length is not None and body_length < content_length) or \
                content_length is None:
            try:
                new_data = self.sock.recv(4096)
            except:
                break

            if new_data == b'':
                break

            if (content_length is None and body_length is None) and \
                    HttpContentType.html.value.encode('ASCII') not in new_data:
                return HttpResponse(status_code=400, reason_message="Content type is not text/html")

            response_raw += new_data
            response.construct_from_string(response_raw.decode('ASCII', errors="ignore"))

            if response.content_type != HttpContentType.html:
                return HttpResponse(status_code=400, reason_message="Content type is not text/html")

            content_length = response.content_length
            body_length = len(response_raw.split(b'\r\n\r\n')[1])

        self.sock.close()
        response = HttpResponse()
        response.construct_from_string(response_raw.decode('ASCII', errors="ignore"))

        if response.status_code == 301 or response.status_code == 302:
            if response.location is None:
                return HttpResponse(status_code=400, reason_message="Redirection failed, Location header not found")
            sys.stderr.write("Redirected to: " + response.location + '\n')
            return self.get(response.location, recursion_count=recursion_count + 1)

        if response.content_type is None:
            return HttpResponse(status_code=400, reason_message="Content-Type header not found")
        if response.content_type is not HttpContentType.html:
            return HttpResponse(status_code=400, reason_message="Content type is not text/html")
        return HttpResponse(status_code=response.status_code, reason_message=response.reason_message,
                            body=response.body)
