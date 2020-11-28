from http import client


class HttpInfo:
    def __init__(self, ws: str):
        self.url = ws

    def get_info(self) -> tuple:
        http_server = None
        insecure_http = True
        redirect_to_https = False

        try:
            response = self.get_http()
            http_server = self.get_header(response=response, header="Server")

            redirect_count = 0

            while 300 <= response.status < 310 and redirect_count < 10:
                self.url = self.get_header(response=response, header="Location")

                if self.url is not None:
                    if len(self.url) > 8 and self.url[0:8] == "https://":
                        redirect_to_https = True
                        break
                        # response = self.get_https()
                    else:
                        response = self.get_http()
                else:
                    break

                redirect_count += 1
        except:
            insecure_http = False
            try:
                response = self.get_https()
                http_server = self.get_header(response=response, header="Server")
            except:
                pass

        return http_server, insecure_http, redirect_to_https

    @staticmethod
    def get_header(response: client.HTTPResponse, header: str):
        for h in response.getheaders():
            if h[0].lower() == header.lower():
                return h[1]

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
            res = url.split(':')[1][2:]
            if res[-1] == '/':
                return res[:-1]
            else:
                return res
        else:
            return url
