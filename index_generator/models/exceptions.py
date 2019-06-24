class IndexGeneratorBaseException(BaseException):
    def __init__(self, message, hint='Something went wrong.'):
        super().__init__(message)
        self.hint = hint


class IndexGeneratorTemplateNotFound(IndexGeneratorBaseException):
    def __init__(self, message):
        super().__init__(message, hint='Template folder does not exists or template file is not found.')


class IndexGeneratorPathNotExists(IndexGeneratorBaseException):
    def __init__(self, message):
        super().__init__(message, hint='Target path does not exists.')
