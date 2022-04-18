class OpenBDConnectionError(Exception):

    def __init__(self):
        super().__init__()
        self.message = "OpenBD API endpoint is connection error."

class OpenBD404NotFoundError(Exception):

    def __init__(self):
        super().__init__()
        self.message = "OpenBD API endpoint is 404 not found."
