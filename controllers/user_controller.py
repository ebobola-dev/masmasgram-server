from aiohttp import web
from socketio import AsyncServer
from traceback import format_exc

from config.strings import *
from models.user import User
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
		except:
			print(f'[CHECK USERNAME IS EXISTS] UNEXCEPTED error: {format_exc()}')
			return web.json_response(
				status=500,
				data=UNEXCEPTED_SERVER_ERROR_MESSAGE,
			)

	async def get_my_user_data(self, request: web.Request):
		try:
			user_id = request.get('authorized_data').get('id')
			database_user = DatabaseService.user_collection.find_one({ '_id': user_id })
			if database_user is None:
				return web.json_response(
					status=400,
					data='Данные не найдены',
				)
			user = User.from_database_view(database_user)
			return web.json_response(
				data=user.to_client_view(),
			)
		except:
			print(f'[get_my_user_data] UNEXCEPTED error: {format_exc()}')
			return web.json_response(
				status=500,
				data=UNEXCEPTED_SERVER_ERROR_MESSAGE,
			)

	async def get_users(self, request: web.Request):
		try:
			database_users = DatabaseService.user_collection.find()
			if database_users is None:
				return web.json_response(
					status=400,
					data='Данные не найдены',
				)
			users = tuple(map(
				lambda database_user: User.from_database_view(database_user).to_client_view(),
				tuple(database_users),
			))
			return web.json_response(
				data=users,
			)
		except:
			print(f'[get_users] UNEXCEPTED error: {format_exc()}')
			return web.json_response(
				status=500,
				data=UNEXCEPTED_SERVER_ERROR_MESSAGE,
			)

	async def get_user(self, request: web.Request):
		try:
			target_username = request.rel_url.query.get('username')
			target_username_validation_error = await Validations.username_validation(username=target_username, is_new=False)
			if target_username_validation_error is not None:
				return web.json_response(
					status=400,
					data={
						'error': target_username_validation_error,
					},
				)
			database_user = DatabaseService.user_collection.find_one({ 'username': target_username })
			if database_user is None:
				return web.json_response(
					status=400,
					data={
						'error': "Пользователь с указанным username не найден",
					},
				)
			target_user = User.from_database_view(database_user)
			return web.json_response(
				data=target_user.to_client_view(),
			)
		except:
			print(f'[get_user] UNEXCEPTED error: {format_exc()}')
			return web.json_response(
				status=500,
				data=UNEXCEPTED_SERVER_ERROR_MESSAGE,
			)