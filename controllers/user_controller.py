from io import BytesIO
from PIL import Image
from aiohttp import web
from socketio import AsyncServer
from traceback import format_exc

from config.filepaths import FILEPATHS
from services.database import DatabaseService
from services.validations import Validations

class UserController:
	def __init__(self, sio: AsyncServer):
		self.sio = sio

	async def check_username_is_exists(self, request: web.Request):
		try:
			username: str | None = request.rel_url.query.get('username')
			username_validation_error = await Validations.username_validation(username=username, is_new=False)
			if username_validation_error is not None:
				return web.json_response(
					status=400,
					data={'error': username_validation_error},
				)
			user = DatabaseService.user_collection.find_one({ 'username': username })
			return web.json_response(
				data={
					'username': username,
					'is_exists': user is not None,
				},
			)
		except Exception as error:
			print(f'[CHECK USERNAME IS EXISTS] UNEXCEPTED error: {error}')
			return web.json_response(
				status=500,
				data='unexpected server error',
			)

	async def upload_image_test_func(self, request: web.Request):
		try:
			body: dict = await request.post()
			image = body.get('image')
			image_ext = body.get('image_ext')
			if image is not None:
				image_content = image.file.read()
				pil_image = Image.open(BytesIO(image_content))
				pil_image.save(f'{FILEPATHS.USER_AVATARS}/some_id{image_ext}')
			return web.json_response(
				data={
					'aboba': 123,
				},
			)
		except Exception as error:
			print(f'[upload_image_test_func] UNEXCEPTED error: {format_exc()}')
			return web.json_response(
				status=500,
				data='unexpected server error',
			)