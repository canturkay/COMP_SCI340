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


class QueryParameter:
    parameter = None
    value = None

    def __init__(self, parameter, value):
        self.parameter = parameter
        self.value = value


def get_header(line: str) -> HttpMessageHeader:
    line_values = line.split(' ')
    if len(line_values) >= 2:
        header_key = line_values[0][:-1]
        header_value = ' '.join(line_values[1:])
        return HttpMessageHeader(header_key, header_value)
    else:
        return HttpMessageHeader(None, None)
