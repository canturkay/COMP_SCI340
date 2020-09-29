import os
import socket
import select
import datetime

from packages.http_params import HttpMethod, HttpContentType
from packages.http_request import HttpRequest
from packages.http_response import HttpResponse


class DynamicWebServer:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def open_connection(self, port: int):
        self.sock.bind(('', port))

        self.sock.listen(10)

        read_list = [self.sock]

        while read_list:
            reads, writes, exceptions = select.select(read_list, [], read_list)

            for read in reads:
                if read is self.sock:
                    conn, addr = self.sock.accept()
                    print("Connected", addr)
                    conn.setblocking(0)
                    read_list.append(conn)
                else:
                    data = read.recv(4096)
                    if not data:
                        read_list.remove(read)
                        read.close()
                        break
                    else:
                        self.process_request(data, conn)

    def process_request(self, data, conn: socket):
        message = HttpRequest()
        message.construct_from_string(data.decode('ASCII'))
        message.content_length = 0

        if message.http_method != HttpMethod.GET:
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
        else:
            query_params = message.address.split('?')[1]


            response_body = '{"operation": "product","operands": [12, 60, 0.5],"result": 360}'


            response = HttpResponse(
                'HTTP/1.1',
                200,
                "OK",
                HttpContentType.json,
                len(response_body.encode('ASCII')),
                datetime.datetime.utcnow(),
                None,
                None,
                response_body
            )

            conn.sendall(str(response).encode('ASCII'))
