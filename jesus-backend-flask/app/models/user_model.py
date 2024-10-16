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
    def find_all():
        try:
            users_list = []
            for user in mongo.db.user.find():
                user["_id"] = str(user["_id"])
                users_list.append(user)
            return users_list
        except PyMongoError as e:
            print(f"Error al obtener los usuarios: {e}")
            return None
        
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
        
    @staticmethod
    def update(user_email, data):
        try:
            update_fields = {k: v for k, v in data.items() if k != "password"}
            if "birthday" in data:
                update_fields["age"] = calculateAge(data['birthday'])
            if "password" in data:
                update_fields["password"] = User.generate_password_hash(data['password'])

            result = mongo.db.user.update_one(
                {"email": user_email},
                {"$set": update_fields}
            )
            return result
        except PyMongoError as e:
            print(f"Error al actualizar usuario: {e}")
            return False
        
    @staticmethod
    def delete(user_email):
        try:
            return mongo.db.user.delete_one({"email": user_email})
        except PyMongoError as e:
            print(f"Error al eliminar usuario: {e}")
            return False