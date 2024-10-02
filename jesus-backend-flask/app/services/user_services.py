from app import mongo
from werkzeug.security import generate_password_hash
from pymongo.errors import PyMongoError
import datetime

def save_user(data):
    try:
        user_data = {
            'nombre': data.nombre,
            'apellido': data.apellido,
            'correo': data.correo,
            'contrasena': generate_password_hash(data.contrasena),
            'genero': data.genero,
            'fecha_nacimiento': data.fecha_nacimiento,
            'edad': calculateAge(data.fecha_nacimiento)
        }
        user_created = mongo.db.user.insert_one(user_data)
        mongo.db.user.create_index([('correo', 1)], unique=True)
        return user_created
    except PyMongoError as e:
        print(f"Error al crear un usuario: {e}")
        return None
    
def calculateAge(fecha_nacimiento):
    try:
        today = datetime.date.today()
        birth_date = datetime.datetime.strptime(fecha_nacimiento, '%Y-%m-%d').date()
        age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
        return age
    except PyMongoError as e:
        print(f"Error en el calculo de edad: {e}")
        return False