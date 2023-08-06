from ciperror import BaseCipError


class UploadFileError(BaseCipError):
    def __init__(self, message):
        super().__init__(
            code="FTE001",
            message="Erro ao realizar upload do arquivo na EF: {}".format(message),
            friendly_message="Erro ao realizar upload do arquivo",
            http_status=500)
