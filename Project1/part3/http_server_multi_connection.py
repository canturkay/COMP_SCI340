import socket

class HttpServerMultiConnection:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    def open_connection(self, port: int):
        print(port)