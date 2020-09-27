import os
import socket
import datetime
from packages.http_request import HttpRequest
from packages.http_params import HttpMessageHeader, HttpMethod, HttpContentType
from packages.http_response import HttpResponse


class HttpServer:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def open_connection(self, port: int):
        self.sock.bind(('', port))

        self.sock.listen()

        while True:
            conn, addr = self.sock.accept()
            with conn:
                print('Connected by', addr)
                while True:
                    data = conn.recv(4096)

                    if not data:
                        break

                    message = HttpRequest()
                    message.construct_from_string(data.decode('ASCII'))

                    skip_message = False

                    if message.http_method != HttpMethod.GET:
                        # print("Request is not a get request")
                        # print(data)
                        response_body = "\"Only GET method is supported\""
                        response = HttpResponse(
                            'HTTP/1.1',
                            400,
                            "Bad Request",
                            HttpContentType.json,
                            len(response_body.encode('ASCII')),
                            datetime.datetime.utcnow(),
                            None,
                            None,
                            response_body
                        )
                        conn.sendall(str(response).encode('ASCII'))

                        skip_message = True

                    if message.address[-4:] != ".htm" and message.address[-5:] != ".html":
                        # print("The request is not for an HTML file")
                        # print(data)
                        response_body = "\"An html file should be requested\""

                        response = HttpResponse(
                            'HTTP/1.1',
                            400,
                            "Bad Request",
                            HttpContentType.json,
                            len(response_body.encode('ASCII')),
                            datetime.datetime.utcnow(),
                            None,
                            None,
                            response_body
                        )
                        conn.sendall(str(response).encode('ASCII'))

                        skip_message = True

                    if not skip_message:
                        file_name = message.address[1:]
                        response_body = self.read_file(file_name)

                        response = HttpResponse(
                            'HTTP/1.1',
                            200,
                            "OK",
                            HttpContentType.html,
                            len(response_body.encode('ASCII')),
                            datetime.datetime.utcnow(),
                            None,
                            None,
                            response_body
                        )
                        # print(response)

                        conn.sendall(str(response).encode('ASCII'))

    @staticmethod
    def read_file(file_name: str) -> str:
        file = open('part2/files/' + file_name, 'r')
        file_content = file.read()
        file.close()

        return file_content
