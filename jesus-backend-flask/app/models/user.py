from app import mongo
from pymongo.errors import PyMongoError
from app.services.user_services import calculateAge

class User:
    def __init__(self, nombre, apellido, correo, contrasena, genero, fecha_nacimiento):
        self.nombre = nombre
        self.apellido = apellido
        self.correo = correo
        self.contrasena = contrasena
        self.genero = genero
        self.fecha_nacimiento = fecha_nacimiento
        self.edad = None

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
    def find_by_email(correo):
        try:
            user = mongo.db.user.find_one({"correo": correo})
            if user:
                user["_id"] = str(user["_id"])
            return user
        except PyMongoError as e:
            print(f"Error al obtener usuario: {e}")
            return None
        
    @staticmethod
    def update(user_correo, data):
        try:
            update_fields = {k: v for k, v in data.items() if k != "password"}
            if "fecha_nacimiento" in data:
                update_fields["edad"] = calculateAge(data['fecha_nacimiento'])
            if "password" in data:
                update_fields["password"] = User.generate_password_hash(data['password'])

            result = mongo.db.user.update_one(
                {"correo": user_correo},
                {"$set": update_fields}
            )
            return result
        except PyMongoError as e:
            print(f"Error al actualizar usuario: {e}")
            return False
        
    @staticmethod
    def delete(user_correo):
        try:
            return mongo.db.user.delete_one({"correo": user_correo})
        except PyMongoError as e:
            print(f"Error al eliminar usuario: {e}")
            return False