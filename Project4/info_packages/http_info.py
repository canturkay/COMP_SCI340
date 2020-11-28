from http import client


class HttpInfo:
    def __init__(self, ws: str):
        self.url = ws
        self.get_info()
        pass

    def get_info(self):
        response = self.get_http()

        while 300 <= response.status < 400:
            self.url = self.get_location_header(response)

            if self.url is not None:
                if len(self.url) > 8 and self.url[0:8] == "https://":
                    response = self.get_https()
                else:
                    response = self.get_http()
            else:
                break

        pass

    @staticmethod
    def get_location_header(response: client.HTTPResponse):
        for header in response.getheaders():
            if header[0] == "Location":
                return header[1]

        return None

    def get_http(self) -> client.HTTPResponse:
        connection = client.HTTPConnection(self.get_hostname(self.url), timeout=2)
        connection.request(method="GET", url=self.get_hostname(self.url))

        response = connection.getresponse()

        connection.close()

        return response

    def get_https(self) -> client.HTTPResponse:
        connection = client.HTTPSConnection(self.get_hostname(self.url), timeout=2)
        connection.request(method="GET", url=self.get_hostname(self.url))

        response = connection.getresponse()

        connection.close()

        return response

    @staticmethod
    def get_hostname(url: str) -> str:
        if 'http' in url:
            return url.split(':')[1][2:]
        else:
            return url
