import jwt
import bcrypt
from aiohttp import web
from socketio import AsyncServer
from traceback import format_exc

from models.user import User
from config.strings import *
from config.server import ServerConfig
from services.validations import Validations
from services.database import DatabaseService
from services.image import ImageService



def _generateAccessToken(id: str):
	payload = {
		'id': id,
	}
	return jwt.encode(
		payload=payload,
		key=ServerConfig.JWT_SECRET_KEY,
		algorithm=ServerConfig.JWT_ENCODE_ALGORITM,
	)

class AuthController:
	def __init__(self, sio: AsyncServer):
		self.sio = sio

	async def registration(self, request: web.Request):
		try:
			body: dict = await request.post()
			username = body.get('username')
			password = body.get('password')
			fullname = body.get('fullname')
			avatar = body.get('avatar')
			avatar_ext = body.get('avatar_ext')
			print(f'[REGISTRATION] Got username: {username}, fullname: {fullname}, avatar_ext: {avatar_ext}')
			validation_errors = tuple(
				filter(
					lambda validation_error: validation_error is not None,
					(
						await Validations.username_validation(username),
						Validations.password_validation(password),
						Validations.fullname_validation(fullname),
						Validations.image_validation(image=avatar, image_ext=avatar_ext),
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

			#? Hashing password and create new user object
			hashed_password = bcrypt.hashpw(password.encode('ascii'), salt=ServerConfig.PASSWORD_HASHING_SALT)
			new_user = User.new(
				username=username,
				password=hashed_password,
				fullname=fullname,
			)

			#? Saving avatar if exists
			is_avatar_saved = False
			if avatar is not None:
				try:
					avatar_local_filepath = ImageService.save_avatar(
						user_id=new_user.id,
						avatar=avatar,
						avatar_ext=avatar_ext,
					)
					new_user.avatar_path = avatar_local_filepath
					is_avatar_saved = True
				except:
					print(f'[REGISTRATION] Error on saving avatar: {format_exc()}')

			#? Save new user in database
			DatabaseService.user_collection.insert_one(new_user.to_database_view())

			print(f'[REGISTRATION] Successfully registered: @{username} "{fullname}"')
			return web.json_response(
				data={
					'is_avatar_saved': is_avatar_saved,
				},
			)
		except:
			print(f'[REGISTRATION] UNEXCEPTED error: {format_exc()}')
			return web.json_response(
				status=500,
				data=UNEXCEPTED_SERVER_ERROR_MESSAGE,
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
		except:
			print(f'[LOGIN] UNEXCEPTED error: {format_exc()}')
			return web.json_response(
				status=500,
				data=UNEXCEPTED_SERVER_ERROR_MESSAGE,
			)

