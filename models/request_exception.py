class RequestException:
	def __init__(
		self,
		code: int,
		eu_message: str,
		ru_message: str,
	):
		self.code = code
		self.eu_message = eu_message
		self.ru_message = ru_message