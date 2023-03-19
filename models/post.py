from datetime import datetime
from uuid import uuid4

from utils.models import ModelsUtils

class Post:
	def __init__(
			self,
			id: str,
			from_user: str,
			date: datetime | str,
			imageUrl: str,
			description: str | None = None,
			likes: list[str] = [],
			comments: list[str] = [],
			favorites: list[str] = [],
	):
		self.id = id
		self.from_user = from_user
		self.date = ModelsUtils.to_datetime(date)
		self.imageUrl = imageUrl
		self.description = description
		self.likes = likes
		self.comments = comments
		self.favorites = favorites

	@staticmethod
	def new(
		from_user: str,
		imageUrl: str,
		description: str | None = None,
	):
		return Post(
			id=str(uuid4()),
			from_user=from_user,
			date=datetime.now(),
			imageUrl=imageUrl,
			description=description,
		)

	def to_database_view(self):
		return ModelsUtils.model_to_database_view(model=self)

	@staticmethod
	def from_database_view(database_post: dict):
		return Post(**ModelsUtils.database_view_to_model_dict(database_post))

	def to_client_view(self):
		return ModelsUtils.model_to_client_view(model=self)