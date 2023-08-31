class Response:
    def __init__(self, statusCode, body):
        self.statusCode = statusCode
        self.body = body
        self.headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
        }
