from part1.http_response import HttpResponse
import socket


class HttpHandler:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def get(self, url: str, recursion_count: int = 0) -> HttpResponse:
        if recursion_count >= 10:
            return HttpResponse(408, "Recursion limit of 10 exceeded", "")

        url_arr = url.split("/")
        base = url_arr[2]
        addr = "/".join(url_arr[3:])

        self.sock.connect((base, 80))

        request = "GET /" + addr + " HTTP/1.1\r\nHost:" + base + "\r\n\r\n"
        self.sock.sendall(request.encode())

        response = (self.sock.recv(4096))
        lines = response.split(b'\r\n')
        response_info = lines[0]

        for line in lines:
            print(line)

        request_version = response_info.split(b' ')[0]
        status_code = response_info.split(b' ')[1]
        reason_message = response_info.split(b' ')[2]

        if status_code == b'301' or status_code == b'302':
            new_url_line = self.get_header(b'Location:', lines)
            if new_url_line is None or new_url_line.find(b':') == -1:
                return HttpHandler(400, "Redirection failed, Location header not found")
            new_url = new_url_line.split(b':')[1]
            return self.get(new_url, recursion_count=recursion_count + 1)

        content_type_line = self.get_header("Content-type:", lines)

        if content_type_line is not None:
            if content_type_line is None or content_type_line.find(b':') == -1:
                return HttpHandler(400, "Content-Type header not found")
            content_type = content_type_line.split(b' ')[1]
            if content_type != b'text/html;':
                return HttpResponse(400, "Content type is not text/html")
        else:
            return HttpResponse(400, "Content type is not text/html")

        

    @staticmethod
    def get_header(header_name: str, lines: list) -> str:
        for line in lines:
            if line.length >= 13 and line[0:13] == header_name:
                return line
        return None
