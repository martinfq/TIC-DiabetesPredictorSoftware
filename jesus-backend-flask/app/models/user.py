import re
from app import mongo
from werkzeug.security import generate_password_hash, check_password_hash
from pymongo.errors import PyMongoError, DuplicateKeyError
import datetime

class User:
    def __init__(self, nombre, apellido, correo, contrasena, genero, fecha_nacimiento):
        self.nombre = nombre
        self.apellido = apellido
        self.correo = correo
        self.contrasena = self.set_password(contrasena)
        self.genero = genero
        self.fecha_nacimiento = fecha_nacimiento
        self.edad = None

    def set_password(self, password):
        if self.validate_password(password):
            return generate_password_hash(password)
        else:
            raise ValueError("La contraseña no cumple con los requisitos de seguridad.")

    def check_password(self, password):
        return check_password_hash(self.contrasena, password)
    

    def save(self):
        try:
            user_data = {
                'nombre': self.nombre,
                'apellido': self.apellido,
                'correo': self.correo,
                'contrasena': self.contrasena,
                'genero': self.genero,
                'fecha_nacimiento': self.fecha_nacimiento,
                'edad': self.calculateAge(self.fecha_nacimiento)
            }
            user_created = mongo.db.user.insert_one(user_data)
            mongo.db.user.create_index([('correo', 1)], unique=True)
            return user_created
        except DuplicateKeyError:
            print(f"Error: El correo '{self.correo}' ya está registrado.")
            return None
        except PyMongoError as e:
            print(f"Error al crear un usuario: {e}")
            return None

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
                update_fields["edad"] = User.calculateAge(data['fecha_nacimiento'])
            if "password" in data:
                update_fields["password"] = User.generate_password_hash(data['password'])

            result = mongo.db.user.update_one(
                {"correo": user_correo},
                {"$set": data}
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
    
    @staticmethod
    def calculateAge(fecha_nacimiento):
        try:
            today = datetime.date.today()
            birth_date = datetime.datetime.strptime(fecha_nacimiento, '%Y-%m-%d').date()
            age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
            return age
        except PyMongoError as e:
            print(f"Error en el calculo de edad: {e}")
            return False
        
    @staticmethod
    def validate_email(correo):
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(email_regex, correo) is not None

    @staticmethod
    def validate_password(contraseña):
        password_regex = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'
        return re.match(password_regex, contraseña) is not None