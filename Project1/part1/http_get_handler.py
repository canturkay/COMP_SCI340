from part1.http_response import HttpResponse
import socket


class HttpHandler:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def get(self, url: str, recursion_count: int = 0) -> HttpResponse:
        if recursion_count >= 10:
            return HttpResponse(408, "Recursion limit of 10 exceeded", "")

        url_arr = url.split("/")
        base = url_arr[1]
        print(base)
        addr = "/".join(url_arr[2:])
        print(addr)

        self.sock.connect((base, 80))

        request = "GET /" + addr + " HTTP/1.1\r\nHost:" + base + "\r\n\r\n"
        self.sock.sendall(request.encode())
        print(repr(self.sock.recv(4096)))
        # connection.sendall(data={})