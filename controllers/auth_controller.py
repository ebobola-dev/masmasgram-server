import jwt
from aiohttp import web
from socketio import AsyncServer
from bson.objectid import ObjectId

from config.server import ServerConfig
from services.database.user_database import UserDatabase
from services.validations import Validations

def _generateAccessToken(id: ObjectId):
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
			print(f'[REGISTRATION] Got username: {username}, password: {password}, fullname: {fullname}')
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
			if fullname is not None:
				fullname = fullname.strip()
				if len(fullname.strip()) == 0:
					fullname = None
			print(f'[REGISTRATION] Successfully registered: @{username} "{fullname}"')
			return web.json_response(
				data="Succesfully registered",
			)
		except Exception as error:
			print(f'web_func: get_file, UNEXCEPTED error: {error}')
			return web.json_response(
				status=500,
				data='unexpected server error',
			)

