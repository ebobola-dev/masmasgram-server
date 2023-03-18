from bson.objectid import ObjectId
from datetime import datetime

from utils.models import ModelsUtils
from utils.database import DatabaseUtils

class Message:
	def __init__(
			self,
			id: ObjectId | str,
			chat_id: ObjectId | str,
			from_user: ObjectId | str,
			date: datetime | str,
			text: str,
			viewed: bool = False,
	):
		self.id = ModelsUtils.to_object_id(id)
		self.chat_id = ModelsUtils.to_object_id(chat_id)
		self.from_user = ModelsUtils.to_object_id(from_user)
		self.date = ModelsUtils.to_datetime(date)
		self.text = text
		self.viewed = viewed

	@staticmethod
	def new(
		chat_id: str | ObjectId,
		from_user: str | ObjectId,
		text: str,
	):
		return Message(
			id=ObjectId(),
			chat_id=chat_id,
			from_user=from_user,
			date=datetime.now(),
			text=text,
		)

	def to_database_view(self):
		return DatabaseUtils.model_to_database_view(model=self)

	@staticmethod
	def from_database_view(database_chat: dict):
		return Message(**DatabaseUtils.database_view_to_model_dict(database_chat))