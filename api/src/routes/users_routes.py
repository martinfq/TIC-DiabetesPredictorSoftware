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
    email = data.get('email')
    nuevo_usuario = Usuario(
        fechaNacimiento = data.get('fechaNacimiento'), 
        genero = data.get('genero'), 
        nombre =  data.get('nombre'), 
        password = data.get('password')
    )
    
    #VALIDA QUE NO EXISTA EL DOMINIO DE LOS CAMPOS
    if(email is None or not nuevo_usuario.is_valid):
        return jsonify({'mensaje': 'CUERPO DE LA SOLICITUD INCORRECTO.'}), 400

    #VALIDA QUE NO EXISTA UN USUARIO CON ESE CORREO
    if usuario_existe(email):
        return jsonify({'mensaje': 'ERROR. YA EXISTE UN USUARIO CON ESTE CORREO'}), 400

    connection = redis_connection()

    nuevo_usuario = nuevo_usuario.data()

    connection.hset(f"usuario:{email}", mapping=nuevo_usuario) #HASH DE USUARIOS

    connection.sadd("USUARIOS", email) #Modificar por sets inversos

    connection.connection_pool.disconnect()
    
    return jsonify({'mensaje': 'Usuario creado correctamente', 'usuario': nuevo_usuario}), 200


@app.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    
    if(email is None or password is None):
        return jsonify({'mensaje': 'CREDENCIALES INCORRECTAS.'}), 400

    if(not usuario_existe(email) or not validar_credenciales(email, password)):
        return jsonify({'mensaje': 'CREDENCIALES INCORRECTAS.'}), 400


    #CREACION DEL TOKEN DE USUARIO
    payload = {
        'email': email, 
    }
    token_session = jwt.encode(payload, "passPrueba", algorithm='HS256')

    return jsonify({'token_session': token_session}), 200

