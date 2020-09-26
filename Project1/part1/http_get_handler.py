from part1 import http_response
import socket


class HttpHandler:
    sock = None

    def get(self, url: str, recursion_count: int = 0) -> http_response.HttpResponse:
        if recursion_count >= 10:
            return http_response.HttpResponse(408, "Recursion limit of 10 exceeded", "")

        url_arr = url.split("/")
        base = url_arr[2]
        addr = "/".join(url_arr[3:])

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((base, 80))

        request = "GET /" + addr + " HTTP/1.1\r\nHost:" + base + "\r\n\r\n"
        self.sock.sendall(request.encode())

        response = (self.sock.recv(4096)).decode('ASCII')
        self.sock.close()
        lines = response.split('\r\n')
        response_info = lines[0]

        #for line in lines:
        #    print(line)

        request_version = response_info.split(' ')[0]
        status_code = response_info.split(' ')[1]
        reason_message = response_info.split(' ')[2]

        if status_code == '301' or status_code == '302':
            new_url_line = self.get_header('Location:', lines)
            if new_url_line is None or new_url_line.find(' ') == -1:
                return http_response.HttpResponse(400, "Redirection failed, Location header not found")
            new_url = new_url_line.split(' ')[1]
            return self.get(new_url, recursion_count=recursion_count + 1)

        content_type_line = self.get_header("Content-Type:", lines)

        if content_type_line is not None:
            if content_type_line is None or content_type_line.find(':') == -1:
                return http_response.HttpResponse(400, "Content-Type header not found")
            content_type = content_type_line.split(' ')[1]
            if content_type != 'text/html;':
                return http_response.HttpResponse(400, "Content type is not text/html")
        else:
            return http_response.HttpResponse(400, "Content type is not text/html")

        body = self.get_body(lines)
        return http_response.HttpResponse(status_code, reason_message, body)

    @staticmethod
    def get_header(header_name: str, lines: list) -> str:
        for line in lines:
            if len(line) >= len(header_name) and line[0:len(header_name)] == header_name:
                return line
        return None

    @staticmethod
    def get_body(lines: list) -> str:
        body = ''
        body_found = False
        for line in lines:
            if body_found:
                body += line + "\n"
            if line == '':
                body_found = True
        return body


if __name__ == "__main__":
    pass
