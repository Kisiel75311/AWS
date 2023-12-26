# backend/exceptions.py

class BaseException(Exception):
    status_code = 500
    message = "An error occurred"

    def __init__(self, message=None, status_code=None):
        Exception.__init__(self)
        if message:
            self.message = message
        if status_code:
            self.status_code = status_code


class UserNotFoundException(BaseException):
    status_code = 404
    message = "User not found"


class InvalidPasswordException(BaseException):
    status_code = 401
    message = "Invalid password"
