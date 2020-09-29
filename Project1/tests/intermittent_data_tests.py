import unittest

from packages.http_request import HttpRequest
from packages.request_builder import RequestBuilder


class IntermittentDataTests(unittest.TestCase):
    def test1(self):
        rb = RequestBuilder()
        assert rb.receive_data('1', 'GET') is None
        assert rb.messages['1'].message == 'GET'

        assert rb.receive_data('1', ' /basic.html HTTP/1.1\r\nContent') is None
        assert rb.messages['1'].message == 'GET /basic.html HTTP/1.1\r\nContent'
        assert rb.messages['1'].content_length is None

        assert rb.receive_data('2', 'GET /test.html HTTP/1.1\r\nContent-Length: 4') is None
        assert rb.messages['2'].message == 'GET /test.html HTTP/1.1\r\nContent-Length: 4'
        assert rb.messages['2'].content_length == 4

        assert rb.receive_data('1', '-Length: 12\r\n\r\nHello') is None
        assert rb.messages['1'].message == 'GET /basic.html HTTP/1.1\r\nContent-Length: 12\r\n\r\nHello'
        assert rb.messages['1'].content_length == 12
        assert rb.messages['1'].body_bytes == 5

        assert rb.receive_data('2', '\r\n\r\n') is None
        assert rb.messages['2'].message == 'GET /test.html HTTP/1.1\r\nContent-Length: 4\r\n\r\n'
        assert rb.messages['2'].content_length == 4
        assert rb.messages['2'].body_bytes == 0

        assert rb.receive_data('2', 'YOOO') == 'GET /test.html HTTP/1.1\r\nContent-Length: 4\r\n\r\nYOOO'

        assert rb.receive_data('1', ' WORLD') is None
        assert rb.messages['1'].message == 'GET /basic.html HTTP/1.1\r\nContent-Length: 12\r\n\r\nHello WORLD'
        assert rb.messages['1'].body_bytes == 11
        assert rb.messages['1'].content_length == 12
        assert rb.receive_data('1', '!') == 'GET /basic.html HTTP/1.1\r\nContent-Length: 12\r\n\r\nHello WORLD!'

        rq = HttpRequest()
        rq.construct_from_string('GET /basic.html HTTP/1.1\r\nContent-Length: 12\r\n\r\nHello WORLD!')
        print(rq)


if __name__ == '__main__':
    unittest.main()
