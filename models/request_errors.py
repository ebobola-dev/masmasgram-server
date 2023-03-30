from config.strings import *
from models.validation_error import ValidationError
class RequestException:
	def __init__(
		self,
		code: int,
		ru_errors: tuple[str],
		eu_errors: tuple[str],
	):
		self.code = code
		self.ru_errors = ru_errors
		self.eu_errors = eu_errors

	def toJson(self):
		return self.__dict__

class UnexceptedServerError(RequestException):
	def __init__(self):
		super().__init__(
			code=1,
			ru_errors=(UNEXCEPTED_SERVER_ERROR_MESSAGE_RU,),
			eu_errors=(UNEXCEPTED_SERVER_ERROR_MESSAGE_EU,),
		)

class NotAuthorizedError(RequestException):
	def __init__(self):
		super().__init__(
			code=50,
			ru_errors=('Вы не авторизованы',),
			eu_errors=('You are not authorized',),
		)

class ForbiddenError(RequestException):
	def __init__(self):
		super().__init__(
			code=51,
			ru_errors=('У вас нет доступа',),
			eu_errors=("You don't have access",),
		)

class BadRequestDataError(RequestException):
	def __init__(
		self,
		ru_errors: tuple[str],
		eu_errors: tuple[str],
	):
		super().__init__(
			code=100,
			ru_errors=ru_errors,
			eu_errors=eu_errors,
		)

	@staticmethod
	def from_validation_errors(validation_errors: tuple[ValidationError]):
		return BadRequestDataError(
			ru_errors=tuple(error.ru_message for error in validation_errors),
			eu_errors=tuple(error.eu_message for error in validation_errors),
		)

class IncorrectLoginDataError(RequestException):
	def __init__(self):
		super().__init__(
			code=101,
			ru_errors=['Неверный логин или пароль'],
			eu_errors=['Username or password is incorrect'],
		)

class DataNotFoundError(RequestException):
	def __init__(self):
		super().__init__(
			code=102,
			ru_errors=['Данные не найдены'],
			eu_errors=['Data not found'],
		)

class UserWithUsernameNotFound(RequestException):
	def __init__(self):
		super().__init__(
			code=102,
			ru_errors=['Пользователь с указанным username не был найден'],
			eu_errors=['User with specified username was not found'],
		)