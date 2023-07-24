class InvalidPathError(Exception):
    def __init__(self, message):
        super().__init__(message)


class NotFoundError(Exception):

    def __init__(self, object_type: str, object_not_found_name):
        super().__init__(f"{object_type} with name"
                         f" {object_not_found_name} not found")
