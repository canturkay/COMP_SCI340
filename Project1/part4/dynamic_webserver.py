import os
import socket
import select
import datetime
import json
import sys

from packages.http_params import HttpMethod, HttpContentType
from packages.http_request import HttpRequest
from packages.http_response import HttpResponse


class DynamicWebServer:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    read_list = [sock]

    def open_connection(self, port: int):
        self.sock.bind(('', port))

        self.sock.listen(10)

        while self.read_list:
            reads, writes, exceptions = select.select(self.read_list, [], self.read_list)

            for read in reads:
                if read is self.sock:
                    conn, addr = self.sock.accept()
                    print("Connected", addr)
                    conn.setblocking(0)
                    self.read_list.append(conn)
                else:
                    data = read.recv(4096)
                    if not data or data == '':
                        self.read_list.remove(read)
                        read.close()
                        break
                    else:
                        self.process_request(data, read)

    @staticmethod
    def process_request(data, conn: socket):
        message = HttpRequest()
        err = message.construct_from_string(data.decode('ASCII'))
        if err:
            response_body = "\"Wrong format\""
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
            return

        message.content_length = 0

        print(message.http_method.value + " " + message.address)

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
        else:
            if '?' not in message.address or '=' not in message.address:
                response_body = "\"A parameter should be provided\""
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
            else:
                operation = message.address.split('?')[0][1:]
                query_params = message.address.split('?')[1]

                if query_params:
                    query_params = query_params.split('&')
                    all_nums = True
                    result = 1.0
                    operands = []
                    for qp in query_params:
                        if '=' in qp and len(qp.split('=')[1]) > 0:
                            num = qp.split('=')[1]
                            try:
                                parsed_num = float(num)
                                operands.append(qp.split('=')[0])
                                result *= parsed_num
                            except:
                                all_nums = False
                                break
                        else:
                            all_nums = False

                    if all_nums:
                        if result > sys.float_info.max:
                            result = float('inf')
                        if result < - sys.float_info.max:
                            result = float('-inf')

                        if result == float('inf'):
                            result = "inf"
                        elif result == float('-inf'):
                            result = "-inf"
                        response_body = json.dumps({"operation": operation, "operands": operands, "result": result})

                        if operation == 'product':
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
                        else:
                            response_body = "\"Only product is available\""
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
                    else:
                        response_body = "\"Parameter values should be numeric\""
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
                else:
                    response = HttpResponse(
                        'HTTP/1.1',
                        400,
                        'Bad Request'
                    )
        print(response)
        conn.sendall(str(response).encode('ASCII'))
