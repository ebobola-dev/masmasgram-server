from datetime import datetime
from bson.objectid import ObjectId

from utils.models import ModelsUtils
from utils.database import DatabaseUtils

class Post:
	def __init__(
			self,
			id: ObjectId | str,
			from_user: ObjectId | str,
			date: datetime | str,
			imageUrl: str,
			description: str | None = None,
			likes: list[ObjectId] = [],
			comments: list[ObjectId] = [],
			favorites: list[ObjectId] = [],
	):
		self.id = ModelsUtils.to_object_id(id)
		self.from_user = ModelsUtils.to_object_id(from_user)
		self.date = ModelsUtils.to_datetime(date)
		self.imageUrl = imageUrl
		self.description = description
		self.likes = likes
		self.comments = comments
		self.favorites = favorites

	@staticmethod
	def new(
		from_user: str | ObjectId,
		imageUrl: str,
		description: str | None = None,
	):
		return Post(
			id=ObjectId(),
			from_user=from_user,
			date=datetime.now(),
			imageUrl=imageUrl,
			description=description,
		)

	def to_database_view(self):
		return DatabaseUtils.model_to_database_view(model=self)

	@staticmethod
	def from_database_view(database_chat: dict):
		return Post(**DatabaseUtils.database_view_to_model_dict(database_chat))