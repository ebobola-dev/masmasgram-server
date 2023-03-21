from uuid import uuid4
from datetime import datetime

from models.user import User
from models.chat import Chat
from utils.models import ModelsUtils

class Chat:
	def __init__(
			self,
			id: str,
			messages_count: int,
			users: tuple[str],
			last_message: str = None,
	):
		super().__init__(id)
		self.messages_count = messages_count
		self.users = users
		self.last_message = ModelsUtils.to_object_id(last_message)

	@staticmethod
	def new(
		users: tuple[str],
	):
		return Chat(
			id=str(uuid4()),
			messages_count=0,
			users=users,
		)

	def to_database_view(self):
		return ModelsUtils.model_to_database_view(model=self)

	@staticmethod
	def from_database_view(database_chat: dict):
		return Chat(**ModelsUtils.database_view_to_model_dict(database_chat))

	def to_client_view(self):
		return self.__dict__