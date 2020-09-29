class RequestBuilder:
    messages = {}

    
class UnFinishedRequest:
    message = None
    body_bytes = None

    def receive_data(self, data):
        self.message += data

    def __init__(self, message, body_bytes):
        self.message = message
        self.body_bytes = body_bytes
