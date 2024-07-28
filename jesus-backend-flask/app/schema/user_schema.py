import re
from app.models.user import User
from app import mongo



def validate_user(data):
    required_fields = ['nombre', 'apellido', 'correo', 'contrasena', 'genero', 'fecha_nacimiento']
    errors = []

    # Verifica que los campos no esten vacios
    for field in required_fields:
        if field not in data or not isinstance(data[field], str):
            errors.append(f'{field.capitalize()} is required and must be a string')
    
    # Verifica el contenido de cada campo
    if 'nombre' in data and not validate_nombreApellido(data['nombre']):
        errors.append('El nombre debe ser una cadena de texto.')

    if 'apellido' in data and not validate_nombreApellido(data['apellido']):
        errors.append('El apellido debe ser una cadena de texto.')

    if 'correo' in data and not validate_email(data['correo']):
        errors.append('El formato del correo es inválido.')

    if 'contrasena' in data and not validate_password(data['contrasena']):
        errors.append('La contrasena no cumple con los requisitos de seguridad.')
    
    if 'genero' in data and not validate_genero(data['genero']):
        errors.append('El genero debe ser una M o F.')

    if 'fecha_nacimiento' in data and not validate_fecha(data['fecha_nacimiento']):
        errors.append('ELa fecha es incorrecta.')
        
    # Verificar si el correo ya está registrado en la base de datos
    if 'correo' in data and mongo.db.user.find_one({'correo': data['correo']}):
        errors.append(f"El correo '{data['correo']}' ya está registrado.")

    return errors if errors else None


# Validaciones con REGEX
def validate_email(correo):
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(email_regex, correo) is not None


def validate_password(contraseña):
    password_regex = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'
    return re.match(password_regex, contraseña) is not None


def validate_nombreApellido(nombreApellido):
    password_regex = r'^[A-Za-z]+ [A-Za-z]+$'
    return re.match(password_regex, nombreApellido) is not None


def validate_genero(genero):
    password_regex = r'^[MF]$'
    return re.match(password_regex, genero) is not None


def validate_fecha(fecha):
    password_regex = r'^(0[1-9]|1[0-2])\/(0[1-9]|[12][0-9]|3[01])\/\d{4}$'
    return re.match(password_regex, fecha) is not None