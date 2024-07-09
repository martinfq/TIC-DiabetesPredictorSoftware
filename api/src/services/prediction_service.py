import pickle
import numpy as np
from database.redis_connection import redis_connection


def cargar_modelo():
    try:
        with open('modelo.pkl', 'rb') as file:
            modelo_cargado = pickle.load(file)
        return modelo_cargado
    except Exception as e:
        raise RuntimeError(f"No se pudo cargar el modelo: {str(e)}")


def predecir_diabetes(modelo, data):
    try:

        caracteristicas = np.array([
            data.highBP,
            data.highChol,
            data.bmi,
            data.smoker,
            data.stroke,
            data.heartDiseaseOrAttack,
            data.physActivity,
            data.genHlth,
            data.mentHlth,
            data.physHlth,
            data.age
        ]).astype(float) 

        resultado = modelo.predict(caracteristicas.reshape(1, -1))[0]
        return resultado
    except Exception as e:
        raise RuntimeError(f"Error al hacer la predicción: {str(e)}")


def obtener_predicciones_por_usuario(usuario_id):
    connection = redis_connection()
    claves = connection.keys('prediccion:*')
    predicciones_usuario = []

    for clave in claves:
        if connection.hget(clave, 'usuario') == usuario_id:
            predicciones_usuario.append(connection.hgetall(clave))

    return predicciones_usuario

