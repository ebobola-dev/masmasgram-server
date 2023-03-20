import re
import jwt
from traceback import format_exc

from config.models import *
from config.server import ServerConfig
from services.database import DatabaseService

#? Any function retutns None if all checks passed successfully, else returs error message

#! Function [token_validation] changes request parameters
class Validations:
	username_pattern = re.compile(USERNAME_REGEX_PATTERN)
	@staticmethod
	async def username_validation(username: str | None, is_new: bool = True):
		if username is None:
			return 'Имя пользователя не указано'
		if not isinstance(username, str):
			return f'Имя пользователя должен быть строчным типом'
		if not len(username) in range(USERNAME_MIN_LEN, USERNAME_MAX_LEN + 1):
			return f'Неверная длина имени пользователя (мин: {USERNAME_MIN_LEN}, макс: {USERNAME_MAX_LEN})'
		regex_result = Validations.username_pattern.match(username)
		if regex_result is None:
			return 'Имя пользователя должно начинатся с латинской буквы, также оно может содержать только латиницу, цифры и знак нижнего подчеркивания'
		if is_new:
			username_is_taken = DatabaseService.user_collection.find_one({'username': username}) != None
			if username_is_taken:
				return 'Имя пользователя уже занято'

	@staticmethod
	def password_validation(password: str | None):
		if password is None:
			return 'Пароль не указан'
		if not isinstance(password, str):
			return f'Пароль должен быть строчным типом'
		if not len(password) in range(PASSWORD_MIN_LEN, PASSWORD_MAX_LEN + 1):
			return f'Неверная длина пароля (мин: {PASSWORD_MIN_LEN}, макс: {PASSWORD_MAX_LEN})'
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

	@staticmethod
	def image_validation(image, image_ext: str):
		if image is None:
			return
		if image_ext is None:
			return 'Расширение фотографии не указано'
		if not isinstance(image_ext, str):
			return 'Расширение фотографии должно быть в виде строки'
		if image_ext not in ALLOWED_IMAGE_EXTENSIONS:
			return f'Неверное расширение фотографии (допустимые: {ALLOWED_IMAGE_EXTENSIONS})'

	@staticmethod
	def token_validation(auth_headers: str | None, request_body: dict):
		error_message = 'Вы не авторизированы'
		try:
			token = auth_headers.split(' ')[1]
			decoden_data = jwt.decode(token, key=ServerConfig.JWT_SECRET_KEY, algorithms=ServerConfig.JWT_ENCODE_ALGORITM)
			request_body['authorized_data'] = decoden_data
		except:
			print(f'error on validation token: {format_exc()}')
			return error_message