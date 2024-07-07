from flask import Blueprint, request, jsonify
from database.redisConnection import redis_connection
import hashlib, uuid
from services.UserService import usuarioExiste

app = Blueprint('users_blueprint', __name__)


@app.route('/registrar', methods=['POST'])
def crearUsuario():
    #LECTURA DE DATOS DESDE EL QUERY
    data = request.json 
    fechaNacimiento = data.get('fechaNacimiento')
    genero = data.get('genero')
    nombre = data.get('nombre')
    email = data.get('email')
    password = data.get('password')
    
    #VALIDA QUE NINGUNO DE LOS CAMPOS SOLICITADOS SEA NULO
    if(fechaNacimiento is None or genero is None or nombre is None or email is None or password is None):
        jsonify({'mensaje': 'CUERPO DE LA SOLICITUD INCORRECTO.'}), 400

    #VALIDAR DOMINIO DE LOS CAMPOS

    #VALIDA QUE NO EXISTA UN USUARIO CON ESE CORREO
    if usuarioExiste(email):
        return jsonify({'mensaje': 'ERROR. YA EXISTE UN USUARIO CON ESTE CORREO'}), 400

    connection = redis_connection()

    #CONSTRUCCION DEL NUEVO OBJETO
    nuevo_usuario = {'fechaNacimiento': fechaNacimiento, 'genero': genero, 'nombre' : nombre, 'email' : email, 'password' : password, }

    usuario_id = str(uuid.uuid4())

    connection.hset(f"usuario:{usuario_id}", mapping=nuevo_usuario) #HASH DE USUARIOS

    connection.sadd("USUARIOS", usuario_id) #Modificar por sets inversos

    connection.connection_pool.disconnect()
    
    return jsonify({'mensaje': 'Usuario creado correctamente', 'usuario': nuevo_usuario}), 200

