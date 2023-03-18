import re
from aiohttp import web

from config.models import *
from services.database.user_database import UserDatabase

#? Any function retutns None if all checks passed successfully, else returs error message
class Validations:
	username_pattern = re.compile(USERNAME_REGEX_PATTERN)
	@staticmethod
	async def username_validation(username: str | None):
		if username is None:
			return 'Имя пользователя не указано'
		if not isinstance(username, str):
			return f'Имя пользователя должен быть строчным типом'
		if not len(username) in range(USERNAME_MIN_LEN, USERNAME_MAX_LEN + 1):
			return f'Неверная длина имени пользователя (мин: {USERNAME_MIN_LEN}, макс: {USERNAME_MAX_LEN})'
		regex_result = Validations.username_pattern.match(username)
		if regex_result is None:
			return 'Имя пользователя должно начинатся с латинской буквы, также оно может содержать только латиницу, цифры и знак нижнего подчеркивания'
		if UserDatabase.username_is_taken(username):
			return 'Имя пользователя уже занято'

	@staticmethod
	def password_validation(password: str | None):
		if password is None:
			return 'Пароль не указан'
		if not isinstance(password, str):
			return f'Пароль должен быть строчным типом'
		if not len(password) in range(PASSWORD_MIN_LEN, PASSWORD_MAX_LEN + 1):
			return 'Неверная длина пароля'
		if ' ' in password:
			return 'Пароль не должен содержать пробелы'

	@staticmethod
	def fullname_validation(fullname: str | None):
		if fullname is None:
			return
		if not isinstance(fullname, str):
			return f'Имя должно быть строчным типом'
		fullname = fullname.strip()
		if not len(fullname) in range(FULLNAME_MAX_LENGTH + 1):
			return f'Максимальная длина имени: {FULLNAME_MAX_LENGTH}'