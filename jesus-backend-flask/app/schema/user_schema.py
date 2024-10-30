import re
from app.models.user_model import User
from app import mongo
from werkzeug.security import check_password_hash


def validate_login(data):
    required_fields = ['email', 'password']
    errors = []

    # Verifica que los campos no esten vacios
    for field in required_fields:
        if field not in data or not isinstance(data[field], str):
            errors.append(f'{field.capitalize()} es requerido')
    
    # Verifica el contenido de cada campo
    if 'email' in data and not mongo.db.user.find_one({'email': data['email']}):
        errors.append(f"El usuario '{data['email']}' no está registrado.")


    if 'email' in data and mongo.db.user.find_one({'email': data['email']}):
        if not check_password_hash(mongo.db.user.find_one({'email': data['email']})['password'], data['password']):
            errors.append(f"Credencianos no validas")

    return errors if errors else None


def validate_user(data):
    required_fields = ['name', 'last_name', 'email', 'password', 'gender', 'birthday']
    errors = []

    # Verifica que los campos no esten vacios
    for field in required_fields:
        if field not in data or not isinstance(data[field], str):
            errors.append(f'{field.capitalize()} is required')
    
    # Verifica el contenido de cada campo
    if 'name' in data and not validate_nombreApellido(data['name']):
        errors.append('El nombre debe ser una cadena de texto.')

    if 'last_name' in data and not validate_nombreApellido(data['last_name']):
        errors.append('El apellido debe ser una cadena de texto.')

    if 'email' in data and not validate_email(data['email']):
        errors.append('El formato del correo es inválido.')

    if 'password' in data and not validate_password(data['password']):
        errors.append('La contrasena no cumple con los requisitos de seguridad.')
    
    if 'gender' in data and not validate_genero(data['gender']):
        errors.append('El genero debe ser Masculino o Femenino.')

    if 'birthday' in data and not validate_fecha(data['birthday']):
        errors.append('La fecha es incorrecta.')
        
    # Verificar si el correo ya está registrado en la base de datos
    if 'email' in data and mongo.db.user.find_one({'email': data['email']}):
        errors.append(f"El correo '{data['email']}' ya está registrado.")

    return errors if errors else None


# Validaciones con REGEX
def validate_email(email):
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(email_regex, email) is not None


def validate_password(password):
    password_regex = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'
    return re.match(password_regex, password) is not None


def validate_nombreApellido(nombreApellido):
    password_regex = r'^[A-Za-z]+( [A-Za-z]+)*$'
    return re.match(password_regex, nombreApellido) is not None


def validate_genero(gender):
    password_regex = r'^(Masculino|Femenino)$'

    return re.match(password_regex, gender) is not None


def validate_fecha(fecha):
    password_regex = r'^([0-9]{4})-([0-9]{1,2})-([0-9]{1,2})$'
    return re.match(password_regex, fecha) is not None
    