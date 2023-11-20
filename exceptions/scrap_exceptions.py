class ScrapException(Exception):
    pass


class MissingTextileClass(ScrapException):
    def __init__(self, msg="Please provide a textile class(natural, synthetic,...)."):
        super().__init__(msg)


class MissingTextileColor(ScrapException):
    def __init__(self, msg="Please provide a textile color."):
        super().__init__(msg)


class MissingTextileType(ScrapException):
    def __init__(self, msg="Please provide a textile type(cotton, polyester,...)."):
        super().__init__(msg)


class MissingTextileDimensions(ScrapException):
    def __init__(self, msg="Please provide dimensions for the scrap."):
        super().__init__(msg)


class InvalidTextileClass(ScrapException):
    def __init__(
        self,
        msg="A textile class is provided but is not a valid class, please provide a valid textile class(natural, "
        "synthetic,...).",
    ):
        super().__init__(msg)


class InvalidTextileType(ScrapException):
    def __init__(
        self,
        msg="A textile type is provided but is not a valid type, please provide a valid textile class(cotton, "
        "polyester,...).",
    ):
        super().__init__(msg)
