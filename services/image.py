from PIL import Image
from io import BytesIO
from os import makedirs
from os.path import exists


from config.filepaths import Filepaths

class ImageService:
	@staticmethod
	def initialize():
		#? Creating images directories if not exists
		for dir_path in Filepaths.MUST_BE_CREATED:
			if not exists(dir_path):
				makedirs(dir_path)

	@staticmethod
	def save_avatar(user_id: str, avatar, avatar_ext: str):
		avatar_content = avatar.file.read()
		pil_avatar = Image.open(BytesIO(avatar_content))
		avatar_local_filepath = f'{Filepaths.USER_AVATARS}/{user_id}{avatar_ext}'
		pil_avatar.save(avatar_local_filepath)
		return avatar_local_filepath