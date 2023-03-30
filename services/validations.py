import re
import jwt

from config.models import *
from config.server import ServerConfig
from services.database import DatabaseService
from utils.models import ModelsUtils
from models.validation_error import ValidationError

#? Any function retutns None if all checks passed successfully, else returs [ValidationError] object

#! Function [token_validation] changes request parameters
class Validations:
	username_pattern = re.compile(USERNAME_REGEX_PATTERN)
	@staticmethod
	async def username_validation(username: str | None, is_new: bool = True):
		if username is None:
			return ValidationError(
				eu_message='Username is not specified',
				ru_message='Имя пользователя не указано',
			)
		if not isinstance(username, str):
			return ValidationError(
				eu_message='Username must be a string type',
				ru_message='Имя пользователя должно быть строчным типом',
			)
		if not len(username) in range(USERNAME_MIN_LEN, USERNAME_MAX_LEN + 1):
			return ValidationError(
				eu_message=f'Invalid username length (min: {USERNAME_MIN_LEN}, max: {USERNAME_MAX_LEN})',
				ru_message=f'Неверная длина имени пользователя (мин: {USERNAME_MIN_LEN}, макс: {USERNAME_MAX_LEN})',
			)
		regex_result = Validations.username_pattern.match(username)
		if regex_result is None:
			return ValidationError(
				eu_message='Username must start with a Latin letter, and it can also contain only Latin letters, numbers, and underscores',
				ru_message='Имя пользователя должно начинатся с латинской буквы, также оно может содержать только латиницу, цифры и знак нижнего подчеркивания',
			)
		if is_new:
			username_is_taken = DatabaseService.user_collection.find_one({'username': username}) != None
			if username_is_taken:
				return ValidationError(
					eu_message='Username is already taken',
					ru_message='Имя пользователя уже занято',
				)

	@staticmethod
	def password_validation(password: str | None):
		if password is None:
			return ValidationError(
				eu_message='Password is not specified',
				ru_message='Пароль не указан',
			)
		if not isinstance(password, str):
			return ValidationError(
				eu_message='Password must be a string type',
				ru_message='Пароль должен быть строчным типом',
			)
		if not len(password) in range(PASSWORD_MIN_LEN, PASSWORD_MAX_LEN + 1):
			return ValidationError(
				eu_message=f'Invalid password length (min: {PASSWORD_MIN_LEN}, max: {PASSWORD_MAX_LEN})',
				ru_message=f'Неверная длина пароля (мин: {PASSWORD_MIN_LEN}, макс: {PASSWORD_MAX_LEN})',
			)
		if ' ' in password:
			return ValidationError(
				eu_message='The password must not contain spaces',
				ru_message='Пароль не должен содержать пробелы',
			)

	@staticmethod
	def fullname_validation(fullname: str | None):
		if fullname is None:
			return
		if not isinstance(fullname, str):
			return ValidationError(
				eu_message='Fullname must be a string type',
				ru_message='Имя должно быть строчным типом',
			)
		fullname = fullname.strip()
		if not len(fullname) in range(FULLNAME_MAX_LENGTH + 1):
			return ValidationError(
				eu_message=f'Max length of fullname: {FULLNAME_MAX_LENGTH}',
				ru_message=f'Максимальная длина имени: {FULLNAME_MAX_LENGTH}',
			)

	@staticmethod
	def image_validation(image, image_ext: str):
		if image is None:
			return
		if image_ext is None:
			return ValidationError(
				eu_message='Image extension not specified',
				ru_message='Расширение фотографии не указано',
			)
		if not isinstance(image_ext, str):
			return ValidationError(
				eu_message='Image extension must be a string type',
				ru_message='Расширение фотографии должно быть в виде строки',
			)
		if image_ext not in ALLOWED_IMAGE_EXTENSIONS:
			return ValidationError(
				eu_message=f'Invalid image extension (allowed: {ALLOWED_IMAGE_EXTENSIONS})',
				ru_message=f'Неверное расширение фотографии (допустимые: {ALLOWED_IMAGE_EXTENSIONS})',
			)

	@staticmethod
	def token_validation(auth_headers: str | None, request_body: dict):
		try:
			token = auth_headers.split(' ')[1]
			decoden_data = jwt.decode(token, key=ServerConfig.JWT_SECRET_KEY, algorithms=ServerConfig.JWT_ENCODE_ALGORITM)
			request_body['authorized_data'] = decoden_data
		except:
			return ValidationError(
				eu_message='You are not authorized',
				ru_message='Вы не авторизованы',
			)

	@staticmethod
	def id_validation(id: str | None, id_name: str = 'id'):
		if id is None:
			return ValidationError(
				eu_message=f'{id_name} is not specified',
				ru_message=f'{id_name} не указан',
			)
		if not ModelsUtils.is_valid_uuid(id=id):
			return ValidationError(
				eu_message=f'{id_name} specified incorrectly',
				ru_message=f'{id_name} указан неверно',
			)
		user_in_database = DatabaseService.user_collection.find_one({ '_id': id})
		if user_in_database is None:
			return ValidationError(
				eu_message=f'User with specified {id_name} not found',
				ru_message=f'Пользователь с указанным {id_name} не найден',
			)