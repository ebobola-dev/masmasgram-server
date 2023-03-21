class ModelException(Exception):
	def __init__(self, message: str):
		self.message = message

class MethodShouldBeOverridden(ModelException):
	def __init__(self):
		super().__init__('Method should be overridden')