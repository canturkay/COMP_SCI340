import os
import datetime
import socket

from packages.http_params import HttpMethod, HttpContentType
from packages.http_request import HttpRequest
from packages.http_response import HttpResponse


class HttpServer:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def open_connection(self, port: int):
        print(port)
        self.sock.bind(('', port))

        self.sock.listen()

        while True:
            conn, addr = self.sock.accept()
            print('Connected by', addr)
            while True:
                data = conn.recv(4096)
                
                if not data:
                    break

                message = HttpRequest()
                message.construct_from_string(data.decode('ASCII'))
                message.content_length = 0

                print(message.http_method.value + " " + message.address)

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
                        403,
                        "Forbidden",
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

                    if response_body is None:
                        response_body = "\"The requested HTML file could not be found\""
                        response = HttpResponse(
                            'HTTP/1.1',
                            404,
                            "Not Found",
                            HttpContentType.json,
                            len(response_body.encode('ASCII')),
                            datetime.datetime.utcnow(),
                            None,
                            None,
                            response_body
                        )
                        # print(response)

                        conn.sendall(str(response).encode('ASCII'))
                    else:
                        response = HttpResponse(
                            'HTTP/1.1',
                            200,
                            "OK",
                            HttpContentType.html,
                            len(response_body.encode('utf-8')),
                            datetime.datetime.utcnow(),
                            None,
                            None,
                            response_body
                        )

                        conn.sendall(str(response).encode('utf-8'))

    @staticmethod
    def read_file(file_name: str) -> str:
        file_name_second_option = None

        if file_name[-4:] == "html":
            file_name_second_option = file_name[:-1]
        elif file_name[-3:] == "htm":
            file_name_second_option = file_name + "l"

        file = None
        if os.path.exists('part2/files/' + file_name):
            file = open('part2/files/' + file_name, 'r')
        elif os.path.exists('part2/files/' + file_name_second_option):
            file = open('part2/files/' + file_name_second_option, 'r')

        if file:
            file_content = file.read()
            file.close()

            return file_content
        return None
