from bson.objectid import ObjectId

from utils.models import ModelsUtils
from utils.database import DatabaseUtils

class User:
	def __init__(
			self,
			id: ObjectId | str,
			username: str,
			fullname: str | None = None,
			is_online: bool = False,
			avatar_url: str | None = None,
			posts: list[ObjectId] = [],
			followers: list[ObjectId] = [],
			follows: list[ObjectId] = [],
	):
		self.id = ModelsUtils.to_object_id(id)
		self.username = username
		self.fullname = fullname
		self.is_online = is_online
		self.avatar_url = avatar_url
		self.posts = posts
		self.followers = followers
		self.follows = follows

	@staticmethod
	def new(
		username: str,
		fullname: str | None = None,
		avatar_url: str | None = None,
	):
		return User(
			id=ObjectId(),
			username=username,
			fullname=fullname,
			is_online=True,
			avatar_url=avatar_url,
		)

	def to_database_view(self):
		return DatabaseUtils.model_to_database_view(model=self)

	@staticmethod
	def from_database_view(database_chat: dict):
		return User(**DatabaseUtils.database_view_to_model_dict(database_chat))