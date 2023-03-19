import asyncio
from socketio import AsyncServer
from aiohttp import web

from config.server import ServerConfig
from services.database.database import DatabaseService
from controllers.auth_controller import AuthController
from controllers.user_controller import UserController

sio = AsyncServer(async_mode='aiohttp', cors_allowed_origins='*')
app = web.Application()
sio.attach(app)

auth_controller = AuthController(sio=sio)
user_controller = UserController(sio=sio)

app.add_routes([
	web.get('/username_is_exists', user_controller.check_username_is_exists),
	web.post('/registration', auth_controller.registration),
	web.post('/login', auth_controller.login),
])

async def main():
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