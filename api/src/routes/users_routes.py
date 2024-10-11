from flask import Blueprint, request, jsonify
import json
from services.user_service import *
from models.usuario import Usuario

app = Blueprint('users_blueprint', __name__)
user_service = UserService()


@app.route('user/register', methods=['POST'])
def crear_usuario():
    #LECTURA DE DATOS DESDE EL QUERY
    data = request.json 
    nuevo_usuario = Usuario(
        fechaNacimiento = data.get('birthday'), 
        genero = data.get('genero', 'M'), 
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

    return jsonify({'token_session': resultado[0]}), 200

