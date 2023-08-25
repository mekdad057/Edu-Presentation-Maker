class InvalidPathError(Exception):
    def __init__(self, message):
        super().__init__(message)


class NotFoundError(Exception):

    def __init__(self, object_type: str, object_not_found_name):
        super().__init__(f"{object_type} with name"
                         f" {object_not_found_name} not found")


class ExtractionError(Exception):
    def __init__(self, file_name, path):
        self.file_name = file_name
        self.path = path
        super().__init__(f"Document '{file_name}' extraction FAILED")
