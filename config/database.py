from utils.yaml_rw import YamlUtil

class DatabaseConfig:
	CONNECTION_URL = 'mongodb://localhost:27017'
	DATABASE_NAME = 'masmasgram'

	@staticmethod
	def initialize(database_config_filepath: str):
		dict_config: dict = YamlUtil.read(filepath=database_config_filepath)
		DatabaseConfig.CONNECTION_URL = dict_config.get('CONNECTION_URL')
		DatabaseConfig.DATABASE_NAME = dict_config.get('DATABASE_NAME')