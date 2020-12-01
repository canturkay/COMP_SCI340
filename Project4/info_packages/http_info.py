from requests import Response, Session

class HttpInfo:
    def __init__(self, ws: str):
        self.url = ws
        self.session = Session()
        self.session.max_redirects = 10

    def get_info(self) -> tuple:
        http_server = None
        insecure_http = True
        redirect_to_https = False
        hsts = False

        try:
            response = self.get_http()

            if 300 <= response.status_code < 310:
                raise Exception("Redirected more than 10 times")

            if response.url[:8] == 'https://':
                redirect_to_https = True

            if self.url == 'amazon.com':
                print(response)

            http_server, hsts = self.process_response(response=response)

        except Exception as ex:
            if ex is not Exception("Redirected more than 10 times"):
                insecure_http = False
                try:
                    response = self.get_https()

                    http_server, hsts = self.process_response(response=response)
                except:
                    pass

        return http_server, insecure_http, redirect_to_https, hsts

    def process_response(self, response: Response) -> tuple:
        http_server = response.headers.get(key='Server')
        hsts_res = response.headers.get(key="Strict-Transport-Security")

        if 'amazon' in self.url:
            print("YOOO")

        if hsts_res is None:
            hsts = False
        else:
            hsts = True

        return http_server, hsts

    def get_https_info(self, http_server: str, hsts: bool) -> tuple:
        response = None
        try:
            response = self.get_https()

            http_server = self.get_header(response=response, header="Server")

            hsts_res = self.get_header(response=response, header="Strict-Transport-Security")

            if hsts_res is None:
                hsts = False
            else:
                hsts = True
        except Exception as ex:
            print(ex)

        return http_server, hsts, response

    @staticmethod
    def get_header(response: Response, header: str):
        for h in response.headers:
            if h[0].lower() == header.lower():
                return h[1]

        return None

    def get_http(self, repeat: int = 0) -> Response:
        try:
            return self.session.get('http://' + self.get_hostname(self.url))
        except:
            if repeat < 3:
                return self.get_http(repeat=repeat+1)
            else:
                return None

    def get_https(self, repeat: int = 0) -> Response:
        try:
            return self.session.get('https://' + self.get_hostname(self.url))
        except:
            if repeat < 3:
                return self.get_http(repeat=repeat+1)
            else:
                return None

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
