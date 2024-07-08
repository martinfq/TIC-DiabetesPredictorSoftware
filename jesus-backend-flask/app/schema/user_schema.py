from app.models.user import User
from app import mongo


def validate_user(data):
    required_fields = ['nombre', 'apellido', 'correo', 'contrasena', 'genero', 'fecha_nacimiento']
    errors = []
    for field in required_fields:
        if field not in data or not isinstance(data[field], str):
            errors.append(f'{field.capitalize()} is required and must be a string')
    
    if 'correo' in data and not User.validate_email(data['correo']):
        errors.append('El formato del correo es inválido.')

    if 'contraseña' in data and not User.validate_password(data['contraseña']):
        errors.append('La contraseña no cumple con los requisitos de seguridad.')
        
    # Verificar si el correo ya está registrado en la base de datos
    if 'correo' in data and mongo.db.user.find_one({'correo': data['correo']}):
        errors.append(f"El correo '{data['correo']}' ya está registrado.")

    return errors if errors else None