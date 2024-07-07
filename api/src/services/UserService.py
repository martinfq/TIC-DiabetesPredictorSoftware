from database.redisConnection import redis_connection

def usuarioExiste(email):
    connection = redis_connection()
    for clave in connection.scan_iter("usuario:*"):
        usuario = connection.hgetall(clave)
        correo_usuario = usuario.get('email')
        if correo_usuario and correo_usuario == email:
            return True
    return False