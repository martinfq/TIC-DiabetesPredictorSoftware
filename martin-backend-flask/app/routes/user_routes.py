from flask import Blueprint, request, jsonify
from ..models.user import User

user_blueprint = Blueprint('user', __name__)


@user_blueprint.route('/register', methods=['POST'])
def register_user():
    data = request.get_json()

    # Lista de campos obligatorios
    required_fields = ['username', 'email', 'nombre', 'apellido', 'contraseña']

    # Verificar si todos los campos obligatorios están presentes
    missing_fields = [field for field in required_fields if field not in data or not data[field]]

    if missing_fields:
        return jsonify({"message": f"Campos incompletos: {', '.join(missing_fields)}"}), 400

    username = data['username']
    email = data['email']
    nombre = data['nombre']
    apellido = data['apellido']
    contraseña = data['contraseña']
    fecha_nacimiento = data.get('fecha_nacimiento')  # Campo opcional

    existing_user = User.get_user_by_email(email)
    if existing_user:
        return jsonify({"message": "User already exists"}), 400

    user = User.create_user(
        username=username,
        email=email,
        nombre=nombre,
        apellido=apellido,
        contraseña=contraseña,
        fecha_nacimiento=fecha_nacimiento
    )
    return jsonify({"email": user.email, "message": "User created successfully"}), 201


@user_blueprint.route('/user/<username>', methods=['GET'])
def get_user(username):
    user = User.get_user_by_username(username)
    if user:
        return jsonify({"username": user.username, "email": user.email}), 200
    return jsonify({"message": "User not found"}), 404


@user_blueprint.route('/user/email/<email>', methods=['GET'])
def get_user_by_email(email):
    user = User.get_user_by_email(email)
    if user:
        return jsonify({"username": user.username, "email": user.email}), 200
    return jsonify({"message": "User not found"}), 404
