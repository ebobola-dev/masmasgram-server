from uuid import uuid4

from utils.models import ModelsUtils
from models.model import MyModel

class User(MyModel):
	def __init__(
			self,
			id: str,
			username: str,
			password: str,
			fullname: str | None = None,
			sid: list[str] = [],
			avatar_path: str | None = None,
			posts: list[str] = [],
			followers: list[str] = [],
			follows: list[str] = [],
	):
		super.__init__(id)
		self.username = username
		self.password = password
		self.fullname = fullname
		self.sid = sid
		self.avatar_path = avatar_path
		self.posts = posts
		self.followers = followers
		self.follows = follows

	@staticmethod
	def new(
		username: str,
		password: str,
		fullname: str | None = None,
	):
		return User(
			id=str(uuid4()),
			username=username,
			password=password,
			fullname=fullname,
		)

	def to_database_view(self):
		return ModelsUtils.model_to_database_view(model=self)

	@staticmethod
	def from_database_view(database_user: dict):
		return User(**ModelsUtils.database_view_to_model_dict(database_user))

	def to_client_view(self):
		client_view = self.__dict__
		client_view.pop('password', None)		#? Removing password field
		client_view.pop('avatar_path', None)	#? Removing avatar_path field

		#? Changing 'sid' field value to 'is_online'
		if 'sid' in client_view.keys():
			client_view['is_online'] = len(client_view.pop('sid')) > 0

		client_view['posts_count'] = len(client_view.pop('posts', []))
		client_view['followers_count'] = len(client_view.pop('followers', []))
		client_view['follows_count'] = len(client_view.pop('follows', []))
		return client_view