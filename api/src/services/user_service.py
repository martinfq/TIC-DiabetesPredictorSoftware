from database.redis_connection import redis_connection

def usuario_existe(email):
    connection = redis_connection()
    if connection.sismember("USUARIOS", email) == 0:
        return False
    return True

def validar_credenciales(email, password):
    connection = redis_connection()
    for clave in connection.scan_iter("usuario:*"):
        usuario = connection.hgetall(clave)
        email_user = clave.split(":")[1]
        password_user = usuario.get('password')
        if email_user == email and password_user == password:
            return True
    return False