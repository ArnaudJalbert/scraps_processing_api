class UserException(Exception):
    pass


class MissingUsername(UserException):
    def __init__(self, message="Username is missing, please provide a username."):
        super().__init__(message)


class UsernameAlreadyUsed(UserException):
    def __init__(
        self, message="Username is already used, please pick a different username."
    ):
        super().__init__(message)


class MissingEmail(UserException):
    def __init__(self, message="Email is missing, please provide an email."):
        super().__init__(message)


class EmailAlreadyUsed(UserException):
    def __init__(self, message="Email is already used, please pick a different email."):
        super().__init__(message)


class MissingPassword(UserException):
    def __init__(self, message="Password is missing, please provide an password."):
        super().__init__(message)


class InstagramAlreadyUsed(UserException):
    def __init__(
        self,
        message="This Instagram account is already used, please pick a different account.",
    ):
        super().__init__(message)


class MissingInstagram(UserException):
    def __init__(
        self,
        message="Instagram account is missing, please provide an Instagram account.",
    ):
        super().__init__(message)


class NotAnInstagramAccount(UserException):
    def __init__(
        self,
        message="This Instagram account does not exist, please use a valid IG account.",
    ):
        super().__init__(message)
