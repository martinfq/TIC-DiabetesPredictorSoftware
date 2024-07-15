from database.redis_connection import redis_connection
import hashlib

def usuario_existe(email):
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

        if email_user == email and password_user == password:
            connection.connection_pool.disconnect()
            return True

    connection.connection_pool.disconnect()
    return False