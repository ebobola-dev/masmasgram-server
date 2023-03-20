from bcrypt import gensalt

from utils.yaml_rw import YamlUtil

class ServerConfig:
	HOST: str | None = None
	PORT: str | None = None
	JWT_SECRET_KEY: str | None = None
	PASSWORD_HASHING_SALT: bytes | None = None
	JWT_ENCODE_ALGORITM: str | None = None

	@staticmethod
	def initialize(server_config_filepath: str):
		dict_config: dict = YamlUtil.read(filepath=server_config_filepath)
		ServerConfig.HOST = dict_config.get('HOST')
		ServerConfig.PORT = dict_config.get('PORT')
		ServerConfig.JWT_SECRET_KEY = dict_config.get('JWT_SECRET_KEY')
		ServerConfig.PASSWORD_HASHING_SALT = gensalt(rounds=dict_config.get('PASSWORD_HASHING_SALT_ROUNDS'))
		ServerConfig.JWT_ENCODE_ALGORITM = dict_config.get('JWT_ENCODE_ALGORITM')