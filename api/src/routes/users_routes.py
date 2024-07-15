from flask import Blueprint, request, jsonify
from database.redis_connection import redis_connection
import hashlib, uuid, json, jwt
from services.user_service import usuario_existe, validar_credenciales
from models.usuario import Usuario

app = Blueprint('users_blueprint', __name__)


@app.route('/registrar', methods=['POST'])
def crear_usuario():
    #LECTURA DE DATOS DESDE EL QUERY
    data = request.json 
    nuevo_usuario = Usuario(
        fechaNacimiento = data.get('fechaNacimiento'), 
        genero = data.get('genero'), 
        nombre =  data.get('nombre'), 
        email = data.get('email'),
        password = data.get('password')
    )
    
    #VALIDACION DEL DOMINIO DE LOS CAMPOS
    if  not nuevo_usuario.is_valid():
        return jsonify({'mensaje': 'CUERPO DE LA SOLICITUD INCORRECTO.'}), 400

    #VALIDACION PARA ASEGURAR UNICIDAD DE USUARIO
    if usuario_existe(nuevo_usuario.email):
        return jsonify({'mensaje': 'ERROR. YA EXISTE UN USUARIO CON ESTE CORREO'}), 400

    connection = redis_connection()
    connection.hset(f"usuario:{str(uuid.uuid4())}", mapping=nuevo_usuario.data())
    connection.sadd("USUARIOS", nuevo_usuario.email)
    connection.connection_pool.disconnect()
    
    return jsonify({'mensaje': 'Usuario creado correctamente'}), 200


@app.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    
    if email is None or password is None:
        return jsonify({'mensaje': 'CREDENCIALES INCORRECTAS.'}), 400

    if not usuario_existe(email) or not validar_credenciales(email, password):
        return jsonify({'mensaje': 'CREDENCIALES INCORRECTAS.'}), 400


    #CREACION DEL TOKEN DE USUARIO
    token_session = jwt.encode({'email': email}, "passPrueba", algorithm='HS256')

    return jsonify({'token_session': token_session}), 200

