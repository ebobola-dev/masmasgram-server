from aiohttp import web

from config.routes import Routes
from services.validations import Validations

class Middlewares:
	@staticmethod
	@web.middleware
	async def authorized(request: web.Request, handler):
		if request.path not in Routes.AUTHORIZED_ROUTES:
			return await handler(request)
		auth_headers = request.headers.get('Authorization')
		validation_error = Validations.token_validation(auth_headers=auth_headers, request_body=request)
		if validation_error is not None:
			return web.json_response(
				status=203,
				data=validation_error,
			)
		return await handler(request)