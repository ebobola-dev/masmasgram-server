from aiohttp import web
from socketio import AsyncServer
from traceback import format_exc

from config.models import *
from models.request_errors import *

class OtherController:
	def __init__(self, sio: AsyncServer):
		self.sio = sio

	async def get_models_settings(self, request: web.Request):
		try:
			return web.json_response(
				data={
					'username': {
						'min_len': USERNAME_MIN_LEN,
						'max_len': USERNAME_MAX_LEN,
					},
					'password': {
						'min_len': PASSWORD_MIN_LEN,
						'max_len': PASSWORD_MAX_LEN,
					},
					'fullname': {
						'min_len': FULLNAME_MIN_LENGTH,
						'max_len': FULLNAME_MAX_LENGTH,
					},
					'allowed_image_extensions': ALLOWED_IMAGE_EXTENSIONS,
				},
			)
		except:
			print(f'[GET MODELS SETTINGS] UNEXCEPTED error: {format_exc()}')
			return web.json_response(
				status=500,
				data=UnexceptedServerError().toJson(),
			)