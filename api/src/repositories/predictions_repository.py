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
            prediction = connection.hgetall(clave)
            prediction['prediction'] = float(prediction['prediction'])
            prediction['BMI'] = float(prediction['BMI'])
            prediction['class'] = int(prediction['class'])
            prediction['Stroke'] = float(prediction['Stroke'])
            prediction['HighBp'] = float(prediction['HighBp'])
            prediction['HighChol'] = float(prediction['HighChol'])
            prediction['Smoker'] = float(prediction['Smoker'])
            prediction['HeartDiseaseorAttack'] = float(prediction['HeartDiseaseorAttack'])
            prediction['PhysActivity'] = int(prediction['PhysActivity'])
            prediction['GenHlth'] = int(prediction['GenHlth'])
            prediction['MentHlth'] = int(prediction['MentHlth'])
            prediction['PhysHlth'] = int(prediction['PhysHlth'])
            predicciones_usuario.append(prediction)

    connection.connection_pool.disconnect()
    return predicciones_usuario


def last_prediction(user_id):
    connection = redis_connection()
    last_predictions = connection.smembers("LAST_PREDICTION")
    key_last_prediction = None

    for up in last_predictions:
        if up.startswith(f"{user_id}"):
            user_last_prediction = up
            break

    key_last_prediction = "prediccion:" + user_last_prediction.split(':')[1]
    last_prediction = connection.hgetall(key_last_prediction)

    connection.connection_pool.disconnect()
    return last_prediction