from database.redis_connection import redis_connection
import hashlib, uuid, json, jwt

def usuario_creado(email):
    connection = redis_connection()
    if connection.sismember("USUARIOS", email) == 0:
        connection.connection_pool.disconnect()
        return False
    
    connection.connection_pool.disconnect()
    return True


def validar_credenciales(email, password):
    connection = redis_connection()
    password = hashlib.sha256(password.encode()).hexdigest()

    for clave in connection.scan_iter("usuario:*"):
        usuario = connection.hgetall(clave)
        email_user = usuario.get('email')
        password_user = usuario.get('password')
        name_user = usuario.get('nombre')

        if email_user == email and password_user == password:
            connection.connection_pool.disconnect()
            return name_user, clave

    connection.connection_pool.disconnect()
    return None


def crear_usuario(nuevo_usuario):
    connection = redis_connection()
    usuario_id = str(uuid.uuid4())
    connection.hmset(f"usuario:{usuario_id}", nuevo_usuario.data())
    connection.sadd("USUARIOS", nuevo_usuario.email)
    connection.sadd("LAST_PREDICTION", f"{usuario_id}:NONE")
    connection.connection_pool.disconnect()

    return 200


def obtener_datos_usuario(user_id):
    connection = redis_connection()
    datos_usuario = None

    for clave in connection.scan_iter("usuario:*"):
        if(clave == user_id):
            usuario = connection.hgetall(clave)
            datos_usuario = {"age" : usuario["fechaNacimiento"], "name" : usuario["nombre"], "gender" : usuario["genero"]}
            break

    connection.connection_pool.disconnect()
    return datos_usuario