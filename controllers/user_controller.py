from aiohttp import web
from socketio import AsyncServer
from bson.objectid import ObjectId

from config.server import ServerConfig
from services.database.user_database import UserDatabase

class UserController:
	def __init__(self, sio: AsyncServer):
		self.sio = sio

	def check_username_is_exists(self, request: web.Request):
		try:
			username: str | None = request.rel_url.query.get('username')
			if username is None:
				return web.json_response(
					status=400,
					data={'error': 'имя пользователя не указано'},
				)
			result = UserDatabase.check_username_is_exists(username)
			return web.json_response(
				data={
					'username': username,
					'is_exists': result,
				},
			)
		except Exception as error:
			print(f'web_func: get_file, UNEXCEPTED error: {error}')
			return web.json_response(
				status=500,
				data='unexpected server error',
			)
