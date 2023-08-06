
class CokoException(Exception):
    pass


class FolderNotFound(CokoException):

    def __init__(self, incorrect_path):
        self.incorrect_path = incorrect_path
