import jwt
from flask import Blueprint, jsonify, request
from app.models.user_model import User
from app.schema.user_schema import validate_user, validate_login
from app.services.user_services import save_user

user_bp = Blueprint('user', __name__)

#============================ USUARIO: CREATE ============================#
@user_bp.route('/user/register', methods=['POST'])
def add_user():
    try:
        data = request.get_json()

        # Validar datos de entrada
        error = validate_user(data)
        if error:
            return jsonify({'error': error}), 400
        
        user = User(
            name=data['name'],
            last_name=data['last_name'],
            email=data['email'],
            password=data['password'],
            gender=data['gender'],
            birthday=data['birthday']
        )
        save_user(user)
        return jsonify({'message': 'Usuario creado correctamente'}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

#============================ USUARIO: LOG IN ============================#

@user_bp.route('/login', methods=['POST'])
def login():
    data = request.json

    email = data.get('email')
    password = data.get('password')
    
    error = validate_login(data)
    if error:
        return jsonify({'error': error}), 400

    #CREACION DEL TOKEN DE USUARIO
    access_token = jwt.encode({'email': email}, "passPrueba", algorithm='HS256')
    return jsonify({'access_token': access_token}), 200

#============================ USUARIO: GET ALL ============================#
@user_bp.route("/users", methods=["GET"])
def get_users():
    users = User.find_all()
    return jsonify(users), 200

#============================ USUARIO: GET BY EMAIL ============================#
@user_bp.route('/user/email/<email>', methods=['GET'])
def get_user(email):
    user = User.find_by_email(email)
    if user:
        return jsonify(user), 200
    else:
        return jsonify({"message": "User not found"}), 404
    
#============================ USUARIO: DELETE ============================#
@user_bp.route('/user/delete_user/<user_email>', methods=['DELETE'])
def delete_user(user_email):
    user = User.find_by_email(user_email)
    if user:
        User.delete(user_email)
        return jsonify({'message': 'User deleted successfully'}), 200
    else:
        return jsonify({'error': 'User not found'}), 404
    
#============================ USUARIO: UPDATE ============================#
@user_bp.route('/user/update_user/<user_email>', methods=['PUT'])
def update_user(user_email):
    data = request.get_json()
    updated_user = User.update(user_email, data)
    if updated_user:
        return jsonify({"message": "User updated"})
    else:
        return jsonify({"message": "User not updated"})