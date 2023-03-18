class DatabaseUtils:
	@staticmethod
	def model_to_database_view(model: object):
		model_database_view = model.__dict__
		model_database_view.update({ '_id': model.id })
		model_database_view.pop('id')
		model_database_view.pop('_collection_name')
		return model_database_view

	@staticmethod
	def database_view_to_model_dict(database_model_view: dict):
		database_model_view['id'] = database_model_view.get('_id')
		database_model_view.pop('_id')
		return database_model_view
