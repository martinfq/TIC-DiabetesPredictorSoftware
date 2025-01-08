from app import mongo
from pymongo.errors import PyMongoError
from app.services.user_services import calculateAge

class User:
    def __init__(self, name, last_name, email, password, gender, birthday):
        self.name = name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.gender = gender
        self.birthday = birthday
        self.age = None

    @staticmethod
    def find_by_email(email):
        try:
            user = mongo.db.user.find_one({"email": email})
            if user:
                user["_id"] = str(user["_id"])
            return user
        except PyMongoError as e:
            print(f"Error al obtener usuario: {e}")
            return None