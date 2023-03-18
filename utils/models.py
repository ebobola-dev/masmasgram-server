from datetime import datetime
from bson.objectid import ObjectId

class ModelsUtils:
	@staticmethod
	def to_object_id(id: ObjectId | str):
		if isinstance(id, ObjectId):
			return id
		else:
			return ObjectId(id)

	@staticmethod
	def to_datetime(date: datetime | str):
		if isinstance(date, datetime):
			return date
		else:
			return datetime.fromisoformat(date)