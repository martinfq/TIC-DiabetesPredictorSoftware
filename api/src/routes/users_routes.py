from flask import Blueprint, request, jsonify
import json
from services.user_service import *
from models.usuario import Usuario

app = Blueprint('users_blueprint', __name__)
user_service = UserService()


@app.route('user/register', methods=['POST'])
def crear_usuario():
    data = request.json 
    nuevo_usuario = Usuario(
        fechaNacimiento = data.get('birthday'), 
        genero = data.get('genero'), 
        nombre =  data.get('name'),
        last_name =  data.get('last_name'),
        email = data.get('email'),
        password = data.get('password')
    )
    resultado = user_service.crear_usuario(nuevo_usuario)

    if resultado[1] != 200:
        return jsonify({'mensaje': resultado[0]}), resultado[1]
    
    return jsonify({'mensaje': 'Usuario creado correctamente'}), 200


@app.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    
    resultado = user_service.generar_tokenSession(email, password)

    if resultado[1] != 200:
        return jsonify({'error': resultado[0]}), resultado[1]
    return jsonify({'access_token': resultado[0]}), 200


@app.route('/user/', methods=['GET'])
def obtener_datos_usuario():
    token_session = request.headers.get('Authorization')
    if not token_session:
        return jsonify({'ERROR': 'TOKEN FALTANTE'}), 401

    try:
        user_id = jwt.decode(token_session.split(" ")[1], "passPrueba", algorithms=['HS256']).get("id")     
        user_data = user_service.datos_usuario(user_id)

        if user_data[1] != 200:
            return jsonify({'error': resultado[0]}), resultado[1]
        return jsonify(user_data[0]), 200
    except jwt.InvalidTokenError:
        return jsonify({'ERROR': 'TOKEN INVALIDO'}), 401