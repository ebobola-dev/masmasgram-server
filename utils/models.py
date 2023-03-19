from uuid import UUID
from datetime import datetime

class ModelsUtils:
	@staticmethod
	def is_valid_uuid(id: str):
		try:
			uuid = UUID(id, version=4)
		except ValueError:
			return False
		return str(uuid) == id

	@staticmethod
	def to_datetime(date: datetime | str):
		if isinstance(date, datetime):
			return date
		else:
			return datetime.fromisoformat(date)

	@staticmethod
	def model_to_database_view(model: object):
		model_database_view = model.__dict__
		model_database_view.update({ '_id': model.id })
		model_database_view.pop('id')
		return model_database_view

	@staticmethod
	def database_view_to_model_dict(database_model_view: dict):
		database_model_view['id'] = database_model_view.get('_id')
		database_model_view.pop('_id')
		return database_model_view

	@staticmethod
	def model_to_client_view(model: object):
		client_view = model.__dict__
		client_view.pop('password', None)	#? if model constrain 'password' field, remove this field
		client_view.pop('avatar_path', None)	#? if model constrain 'avatar_path' field, remove this field

		#? [For User model] if models constrain 'sid' field, change this field value to 'is_online'
		if 'sid' in client_view.keys():
			client_view['is_online'] = len(client_view.pop('sid')) > 0

		#? if model constrain datetime fields, convert this fields to str type
		for key, value in client_view.items():
			if isinstance(value, datetime):
				client_view[key] = client_view[key].isoformat()
		return client_view