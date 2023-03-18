from bson.objectid import ObjectId
from datetime import datetime

from models.user import User
from models.chat import Chat
from utils.models import ModelsUtils
from utils.database import DatabaseUtils

class Chat:
	def __init__(
			self,
			id: ObjectId | str,
			messages_count: int,
			users: tuple[ObjectId],
			last_message: ObjectId | str = None,
	):
		self.id = ModelsUtils.to_object_id(id)
		self.messages_count = messages_count
		self.users = users
		self.last_message = ModelsUtils.to_object_id(last_message)

	@staticmethod
	def new(
		users: str | ObjectId,
	):
		return Chat(
			id=ObjectId(),
			messages_count=0,
			users=users,
		)

	def to_database_view(self):
		return DatabaseUtils.model_to_database_view(model=self)

	@staticmethod
	def from_database_view(database_chat: dict):
		return Chat(**DatabaseUtils.database_view_to_model_dict(database_chat))