class HttpResponse:
    status_code = None
    reason_message = None

    body = None
    headers = None

    def __init__(self, status_code: int, reason_message: str, body:str = None, headers: dict = {}):
        self.status_code = status_code
        self.reason_message = reason_message
        self.body = body
        self.headers = headers


if __name__ == "__main__":
    pass
