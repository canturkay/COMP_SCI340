from enum import Enum


class HttpMessageHeader:
    key = None
    value = None

    def __init__(self, key: str, value):
        self.key = key
        self.value = value


class HttpMethod(Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    unknown = "unknownmethod"


class HttpContentType(Enum):
    html = 'text/html'
    json = 'application/json'
    unknown = 'unknowntype'
