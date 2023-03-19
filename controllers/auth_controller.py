import jwt
import bcrypt
from aiohttp import web
from socketio import AsyncServer

from models.user import User
from config.server import ServerConfig
from services.validations import Validations
from services.database.database import DatabaseService

def _generateAccessToken(id: str):
	payload = {
		'id': id,
	}
	return jwt.encode(payload, ServerConfig.JWT_SECRET_KEY)

class AuthController:
	def __init__(self, sio: AsyncServer):
		self.sio = sio

	async def registration(self, request: web.Request):
		try:
			body: dict = await request.json()
			username = body.get('username')
			password = body.get('password')
			fullname = body.get('fullname')
			print(f'[REGISTRATION] Got username: {username}, fullname: {fullname}')
			validation_errors = tuple(
				filter(
					lambda validation_error: validation_error is not None,
					(
						await Validations.username_validation(username),
						Validations.password_validation(password),
						Validations.fullname_validation(fullname),
					),
				)
			)
			if len(validation_errors):
				print(f'[REGISTRATION] Error: {validation_errors}')
				return web.json_response(
					status=400,
					data={
						'errors': validation_errors,
					},
				)

			#? If fullname is not None, strip it, if stripped fullname is empty => fullname is None
			if fullname is not None:
				fullname = fullname.strip()
				if len(fullname.strip()) == 0:
					fullname = None

			#? Hashing password and create new user object, save new user in database
			hashed_password = bcrypt.hashpw(password.encode('ascii'), salt=ServerConfig.PASSWORD_HASHING_SALT)
			new_user = User.new(
				username=username,
				password=hashed_password,
				fullname=fullname,
			)
			DatabaseService.user_collection.insert_one(new_user.to_database_view())

			print(f'[REGISTRATION] Successfully registered: @{username} "{fullname}"')
			return web.json_response(
				data=new_user.to_client_view(),
			)
		except Exception as error:
			print(f'[REGISTRATION] UNEXCEPTED error: {error}')
			return web.json_response(
				status=500,
				data='unexpected server error',
			)

	async def login(self, request: web.Request):
		try:
			body: dict = await request.json()
			username = body.get('username')
			password = body.get('password')
			print(f'[LOGIN] Got username: {username}')
			validation_errors = tuple(
				filter(
					lambda validation_error: validation_error is not None,
					(
						await Validations.username_validation(username, is_new=False),
						Validations.password_validation(password),
					),
				)
			)
			if len(validation_errors):
				print(f'[LOGIN] Error: {validation_errors}')
				return web.json_response(
					status=400,
					data={
						'error': 'Неверный логин или пароль',
					},
				)

			#? Find user in database by username
			database_user = DatabaseService.user_collection.find_one({ "username": username })
			if database_user is None:
				print(f'[LOGIN] Error: Пользователя с "{username}" юзернеймом не найден')
				return web.json_response(
					status=400,
					data={
						'error': 'Неверный логин или пароль',
					},
				)
			user = User.from_database_view(database_user=database_user)

			#? Checking password
			if not bcrypt.checkpw(password.encode('ascii'), user.password):
				print(f'[LOGIN] Error: @{username} введён неверный пароль')
				return web.json_response(
					status=400,
					data={
						'error': 'Неверный логин или пароль',
					},
				)

			token = _generateAccessToken(id=user.id)
			print(f'[LOGIN] Successfully login: @{username}')
			return web.json_response(
				data={
					'token': token,
				},
			)
		except Exception as error:
			print(f'[LOGIN] UNEXCEPTED error: {error}')
			return web.json_response(
				status=500,
				data='unexpected server error',
			)

