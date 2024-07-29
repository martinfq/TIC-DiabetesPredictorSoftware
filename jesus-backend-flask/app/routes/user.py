import jwt
from flask import Blueprint, jsonify, request
from app.models.user import User
from app.schema.user_schema import validate_user, validate_login

user_bp = Blueprint('user', __name__)

#============================ USUARIO: CREATE ============================#
@user_bp.route('/register', methods=['POST'])
def add_user():
    try:
        data = request.get_json()

        # Validar datos de entrada
        error = validate_user(data)
        if error:
            return jsonify({'error': error}), 400
        
        user = User(
            nombre=data['nombre'],
            apellido=data['apellido'],
            correo=data['correo'],
            contrasena=data['contrasena'],
            genero=data['genero'],
            fecha_nacimiento=data['fecha_nacimiento']
        )
        user.save()
        return jsonify({'message': 'Usuario creado correctamente'}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

#============================ USUARIO: LOG IN ============================#

@user_bp.route('/login', methods=['POST'])
def login():
    data = request.json

    correo = data.get('correo')
    contrasena = data.get('contrasena')
    
    error = validate_login(data)
    if error:
        return jsonify({'error': error}), 400

    #CREACION DEL TOKEN DE USUARIO
    token_session = jwt.encode({'correo': correo}, "passPrueba", algorithm='HS256')
    return jsonify({'token_session': token_session}), 200


#============================ USUARIO: GET ALL ============================#
@user_bp.route("/usuarios", methods=["GET"])
def get_users():
    users = User.find_all()
    return jsonify(users), 200

#============================ USUARIO: GET BY EMAIL ============================#
@user_bp.route('/usuario/<correo>', methods=['GET'])
def get_user(correo):
    user = User.find_by_email(correo)
    if user:
        return jsonify(user), 200
    else:
        return jsonify({"message": "User not found"}), 404
    
#============================ USUARIO: DELETE ============================#
@user_bp.route('/delete_user/<user_correo>', methods=['DELETE'])
def delete_user(user_correo):
    user = User.find_by_email(user_correo)
    if user:
        User.delete(user_correo)
        return jsonify({'message': 'User deleted successfully'}), 200
    else:
        return jsonify({'error': 'User not found'}), 404
    
#============================ USUARIO: UPDATE ============================#
@user_bp.route('/update_user/<user_correo>', methods=['PUT'])
def update_user(user_correo):
    data = request.get_json()
    updated_user = User.update(user_correo, data)
    if updated_user:
        return jsonify({"message": "User updated"})
    else:
        return jsonify({"message": "User not updated"})