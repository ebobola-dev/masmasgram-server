from uuid import uuid4

from utils.models import ModelsUtils

class User:
	def __init__(
			self,
			id: str,
			username: str,
			password: str,
			fullname: str | None = None,
			is_online: bool = False,
			avatar_url: str | None = None,
			posts: list[str] = [],
			followers: list[str] = [],
			follows: list[str] = [],
	):
		self.id = id
		self.username = username
		self.password = password
		self.fullname = fullname
		self.is_online = is_online
		self.avatar_url = avatar_url
		self.posts = posts
		self.followers = followers
		self.follows = follows

	@staticmethod
	def new(
		username: str,
		password: str,
		fullname: str | None = None,
		avatar_url: str | None = None,
	):
		return User(
			id=str(uuid4()),
			username=username,
			password=password,
			fullname=fullname,
			avatar_url=avatar_url,
		)

	def to_database_view(self):
		return ModelsUtils.model_to_database_view(model=self)

	@staticmethod
	def from_database_view(database_user: dict):
		return User(**ModelsUtils.database_view_to_model_dict(database_user))

	def to_client_view(self):
		return ModelsUtils.model_to_client_view(model=self)