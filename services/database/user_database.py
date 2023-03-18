from services.database.database import DatabaseService

class UserDatabase:
    @staticmethod
    def username_is_taken(username: str):
        result = DatabaseService.user_collection.find_one({'username': username})
        return result != None