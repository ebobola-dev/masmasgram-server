from pymongo import MongoClient
from pymongo.database import Database
from pymongo.collection import Collection

from config.database import DatabaseConfig

class DatabaseService:
	connected = False
	database_client: MongoClient | None = None
	database: Database | None = None
	user_collection: Collection | None = None
	post_collection: Collection | None = None
	message_collection: Collection | None = None
	chat_collection: Collection | None = None

	@staticmethod
	def connect():
		DatabaseService.database_client = MongoClient(DatabaseConfig.CONNECTION_URL)
		DatabaseService.database = DatabaseService.database_client.get_database(DatabaseConfig.DATABASE_NAME)
		DatabaseService.user_collection = DatabaseService.database.get_collection('user')
		DatabaseService.post_collection = DatabaseService.database.get_collection('post')
		DatabaseService.message_collection = DatabaseService.database.get_collection('message')
		DatabaseService.chat_collection = DatabaseService.database.get_collection('chat')
		DatabaseService.connected = True