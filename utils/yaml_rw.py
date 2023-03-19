from yaml import safe_load, YAMLError

class YamlUtil:
	@staticmethod
	def read(filepath: str):
		with open(filepath, "r") as yaml_file:
			try:
				return safe_load(yaml_file)
			except YAMLError as exc:
				print(f'Error on read yaml file: {exc}')