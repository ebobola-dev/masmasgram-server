
#? Default parent model class for all database models
import json

from models.exceptions import *

class MyModel:
	def __init__(
		self,
		id: str,
	):
		self.id = id

	@staticmethod
	def new():
		raise MethodShouldBeOverridden()

	def to_database_view(self):
		raise MethodShouldBeOverridden()

	@staticmethod
	def from_database_view():
		raise MethodShouldBeOverridden()

	def to_client_view(self):
		raise MethodShouldBeOverridden()