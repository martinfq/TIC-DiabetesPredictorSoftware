from app import mongo
from werkzeug.security import generate_password_hash
from pymongo.errors import PyMongoError
from datetime import datetime, timezone

def save_user(data):
    try:
        current_time = datetime.now(timezone.utc)
        user_data = {
            'name': data.name,
            'last_name': data.last_name,
            'email': data.email,
            'password': generate_password_hash(data.password),
            'gender': data.gender,
            'birthday': data.birthday,
            'age': calculateAge(data.birthday),
            'timestamp': current_time
        }
        user_created = mongo.db.user.insert_one(user_data)
        mongo.db.user.create_index([('email', 1)], unique=True)
        return user_created
    except PyMongoError as e:
        print(f"Error al crear un usuario: {e}")
        return None
    
def calculateAge(birthday):
    try:
        today = datetime.now()
        birth_date = datetime.strptime(birthday, '%Y-%m-%d').date()
        age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
        return age
    except PyMongoError as e:
        print(f"Error en el calculo de edad: {e}")
        return False