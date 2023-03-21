from datetime import datetime
from uuid import uuid4

from utils.models import ModelsUtils

class Post:
	def __init__(
			self,
			id: str,
			from_user: str,
			date: datetime | str,
			image_paths: list[str],
			description: str | None = None,
			likes: list[str] = [],
			comments: list[str] = [],
			favorites: list[str] = [],
	):
		super().__init__(id)
		self.from_user = from_user
		self.date = ModelsUtils.to_datetime(date)
		self.image_paths = image_paths
		self.description = description
		self.likes = likes
		self.comments = comments
		self.favorites = favorites

	@staticmethod
	def new(
		from_user: str,
		image_paths: str,
		description: str | None = None,
	):
		return Post(
			id=str(uuid4()),
			from_user=from_user,
			date=datetime.now(),
			image_paths=image_paths,
			description=description,
		)

	def to_database_view(self):
		return ModelsUtils.model_to_database_view(model=self)

	@staticmethod
	def from_database_view(database_post: dict):
		return Post(**ModelsUtils.database_view_to_model_dict(database_post))

	def to_client_view(self):
		client_view = self.__dict__
		client_view.pop('image_paths', None)		#? Removing image_paths field

		client_view['date'] = client_view.get('date').isoformat() #? Changing date field to isoformat date

		client_view['likes_count'] = len(client_view.pop('likes', []))
		client_view['comments_count'] = len(client_view.pop('comments', []))
		client_view['favorites_count'] = len(client_view.pop('favorites', []))
		return client_view