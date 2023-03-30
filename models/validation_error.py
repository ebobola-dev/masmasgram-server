class ValidationError:
	def __init__(
		self,
		eu_message: str,
		ru_message: str,
	):
		self.eu_message = eu_message
		self.ru_message = ru_message

	def __repr__(self):
		return f'{self.eu_message}({self.ru_message})'