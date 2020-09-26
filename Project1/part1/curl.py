import sys
from part1 import http_get_handler


def main(argv: list):
    if argv is None or len(argv) != 2:
        wrong_format()

    url = argv[1]

    if len(url) < 7 or url[0:7] != "http://":
        wrong_format()

    http_handler = http_get_handler.HttpHandler()
    response = http_handler.get(url)
    print(response.body)
    if response.body:
        sys.exit(0)
    else:
        sys.exit(2)

def wrong_format():
    print('curl.py http://<url>')
    sys.exit(2)


if __name__ == "__main__":
    main(sys.argv)
