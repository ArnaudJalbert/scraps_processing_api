class ScrapException(Exception):
    pass


class MissingTextileClass(ScrapException):
    def __init__(
        self, message="Please provide a textile class(natural, synthetic,...)."
    ):
        super().__init__(message)


class MissingTextileColor(ScrapException):
    def __init__(self, message="Please provide a textile color."):
        super().__init__(message)


class MissingTextileType(ScrapException):
    def __init__(self, message="Please provide a textile type(cotton, polyester,...)."):
        super().__init__(message)


class MissingScrapOwner(ScrapException):
    def __init__(self, message="Please provide a scrap owner."):
        super().__init__(message)


class MissingTextileDimensions(ScrapException):
    def __init__(self, message="Please provide dimensions for the scrap."):
        super().__init__(message)


class MissingImage(ScrapException):
    def __init__(self, message="Please provide an image of the scrap."):
        super().__init__(message)


class InvalidTextileClass(ScrapException):
    def __init__(
        self,
        message="A textile class is provided but is not a valid class, please provide a valid textile class(natural, "
        "synthetic,...).",
    ):
        super().__init__(message)


class InvalidTextileType(ScrapException):
    def __init__(
        self,
        message="A textile type is provided but is not a valid type, please provide a valid textile class(cotton, "
        "polyester,...).",
    ):
        super().__init__(message)
