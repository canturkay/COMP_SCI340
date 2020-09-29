import socket
import select

class HttpServerMultiConnection:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    def open_connection(self, port: int):
        print(port)
        self.sock.bind(('', port))

        self.sock.listen(2)
        #open_conns = []
        read_list = []
        conn, addr = self.sock.accept()
        read_list.append(conn)
        outputs = []

        while read_list:
            select.select(read_list, outputs)

        while True:
            data = conn.recv(4096)
