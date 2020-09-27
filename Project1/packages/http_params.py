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

    def from_str(self, value: str):
        if value == self.GET.value:
            return self.GET
        elif value == self.POST.value:
            return self.POST
        elif value == self.PUT.value:
            return self.PUT
        elif value == self.DELETE.value:
            return self.DELETE
        else:
            return self.unknown


class HttpContentType(Enum):
    html = 'text/html'
    json = 'application/json'
    unknown = 'unknowntype'

    def from_str(self, value: str):
        if value == self.html.value:
            return self.html
        elif value == self.json.value:
            return self.json
        else:
            return self.unknown
