import sys
from part1.http_get_handler import HttpHandler


def main(argv: list):
    if argv is None or len(argv) != 2:
        wrong_format()

    url = argv[1]

    if len(url) < 7 or url[0:7] != "http://":
        wrong_format()

    http_handler = HttpHandler()
    http_handler.get(url)


def wrong_format():
    print('curl.py http://<url>')
    sys.exit(2)


if __name__ == "__main__":
    main(sys.argv)
