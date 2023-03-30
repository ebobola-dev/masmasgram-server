class ValidationError:
	def __init__(
		self,
		eu_message: str,
		ru_message: str,
	):
		self.eu_message = eu_message
		self.ru_message = ru_message