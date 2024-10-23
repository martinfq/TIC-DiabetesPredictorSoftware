from database.redis_connection import redis_connection
import uuid

def crear_prediccion(prediccion, usuario_id):
    prediccion_id = str(uuid.uuid4())       
    connection = redis_connection()
    connection.hmset(f"prediccion:{prediccion_id}", prediccion) #CREACION DE PREDICCIONES

    #CONSIDERAR SI SE DEFINE CAPTURA Y CONTROL DE EXCEPCIONES A LOS REPOSITORIES, SOBRE TODO A ESTE
    last_predictions = connection.smembers("LAST_PREDICTION")
    user_last_prediction = None

    for up in last_predictions:
        if up.startswith(f"{usuario_id}"):
            user_last_prediction = up
            break
    #CONSIDERAR SI SE AGREGA UNA VALIDACION
    connection.srem("LAST_PREDICTION", user_last_prediction)
    connection.sadd("LAST_PREDICTION", f"{usuario_id}:{prediccion_id}")
    connection.connection_pool.disconnect()

    return 200


def obtener_predicciones(usuario_id):
    connection = redis_connection()
    claves = connection.keys('prediccion:*')
    predicciones_usuario = []

    for clave in claves:
        if connection.hget(clave, 'usuario') == usuario_id:
            predicciones_usuario.append(connection.hgetall(clave))

    return predicciones_usuario