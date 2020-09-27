import sys
from part2.http_server import  HttpServer


def main(argv: list):
    if argv is None or len(argv) != 2:
        wrong_format()

    try:
        port = int(argv[1])

        if port <= 1024:
            print("Port number needs to be higher than or equal to 1024.")
            sys.exit(2)
        else:
            http_server = HttpServer()
            http_server.open_connection(port)
    except:
        wrong_format()


def wrong_format():
    print('http_server1.py <port>')
    sys.exit(2)


if __name__ == "__main__":
    main(sys.argv)
