class HttpBadRequest(Exception):

    def __init__(self, message: str) -> None:

        self.message = message
        self.status_code = 400
        self.name = "BadRequest"