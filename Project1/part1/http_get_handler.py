from part1.http_response import HttpResponse
import socket


class HttpHandler:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def get(self, url: str, recursion_count: int = 0) -> HttpResponse:
        if recursion_count >= 10:
            return HttpResponse(408, "Recursion limit of 10 exceeded", "")

        self.sock.connect(("insecure.stevetarzia.com", 80))

        request = "GET / HTTP/1.1\r\nHost:%s\r\n\r\n" % url
        self.sock.send(request.encode())
        print(self.sock.recv(4096))
        # connection.sendall(data={})

    def open_socket_connection(self, url: str) :
        self.sock.connect((url, 80))
        # connection = None
        #
        # while True:
        #     connection, _ = self.sock.accept()
        #
        # return connection
