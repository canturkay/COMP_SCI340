import socket


class HttpServer:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def open_connection(self, port: int):
        self.sock.bind(('', port))

        self.sock.listen()

        conn, addr = self.sock.accept()
        with conn:
            print('Connected by', addr)
            while True:
                data = conn.recv(1024)
                if not data: break
                conn.sendall(data)
