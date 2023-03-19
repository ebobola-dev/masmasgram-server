from uuid import uuid4
from datetime import datetime

from utils.models import ModelsUtils

class Message:
	def __init__(
			self,
			id: str,
			chat_id: str,
			from_user: str,
			date: datetime | str,
			text: str,
			viewed: bool = False,
	):
		self.id = id
		self.chat_id = chat_id
		self.from_user = from_user
		self.date = ModelsUtils.to_datetime(date)
		self.text = text
		self.viewed = viewed

	@staticmethod
	def new(
		chat_id: str,
		from_user: str,
		text: str,
	):
		return Message(
			id=str(uuid4()),
			chat_id=chat_id,
			from_user=from_user,
			date=datetime.now(),
			text=text,
		)

	def to_database_view(self):
		return ModelsUtils.model_to_database_view(model=self)

	@staticmethod
	def from_database_view(database_message: dict):
		return Message(**ModelsUtils.database_view_to_model_dict(database_message))

	def to_client_view(self):
		return ModelsUtils.model_to_client_view(model=self)