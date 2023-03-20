import asyncio
from socketio import AsyncServer
from aiohttp import web

from config.server import ServerConfig
from config.database import DatabaseConfig
from config.filepaths import Filepaths
from config.routes import Routes
from services.middleware import Middlewares
from services.database import DatabaseService
from services.image import ImageService
from controllers.auth_controller import AuthController
from controllers.user_controller import UserController

async def main():
	ServerConfig.initialize(Filepaths.SERVER_CONFIG)
	DatabaseConfig.initialize(Filepaths.DATABASE_CONFIG)
	ImageService.initialize()

	sio = AsyncServer(async_mode='aiohttp', cors_allowed_origins='*')
	app = web.Application(middlewares=[
		Middlewares.authorized,
	])
	sio.attach(app)

	auth_controller = AuthController(sio=sio)
	user_controller = UserController(sio=sio)

	app.add_routes([
		web.post(Routes.REGISTRATION, auth_controller.registration),
		web.post(Routes.LOGIN, auth_controller.login),
		web.get(Routes.USERNAME_IS_EXISTS, user_controller.check_username_is_exists),
		web.get(Routes.GET_MY_USER_DATA, user_controller.get_my_user_data),
		web.get(Routes.GET_USERS, user_controller.get_users),
		web.get(Routes.GET_USER, user_controller.get_user),
	])

	DatabaseService.connect()

	runner = web.AppRunner(app)
	await runner.setup()
	site = web.TCPSite(
		runner,
		port=ServerConfig.PORT,
		host=ServerConfig.HOST,
	)
	await site.start()
	print(f'Server started on address: {ServerConfig.HOST}:{ServerConfig.PORT}')

	await asyncio.Event().wait()

if __name__ == '__main__':
	asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
	asyncio.run(main())