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

class UserAlreadyExistsError(BaseException):
    status_code = 409
    message = "User already exists"

class GameError(BaseException):
    status_code = 400
    message = "Game error occurred"

    def __init__(self, message=None, status_code=None, additional_info=None):
        super().__init__(message, status_code)
        self.additional_info = additional_info

    def to_dict(self):
        response = {
            'message': self.message,
            'status_code': self.status_code
        }
        if self.additional_info:
            response['additional_info'] = self.additional_info
        return response

class PlayerNotFoundException(BaseException):
    status_code = 404
    message = "Player not found"


class GameNotFoundException(BaseException):
    status_code = 404
    message = "Game not found"


class InvalidMoveException(BaseException):
    status_code = 400
    message = "Invalid move"


class NotYourTurnException(BaseException):
    status_code = 400
    message = "Not your turn"


class GameFullException(BaseException):
    status_code = 400
    message = "Game is full"

