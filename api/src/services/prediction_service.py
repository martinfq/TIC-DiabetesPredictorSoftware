import pickle
import numpy as np
from datetime import datetime
from database.redis_connection import redis_connection
from services.user_service import UserService
from repositories.predictions_repository import crear_prediccion, obtener_predicciones, last_prediction
from models.caracteristicas_prediccion import CaracteristicasPrediccion


def cargar_modelo():
    try:
        with open('modelANN.pkl', 'rb') as file:
            modelo_cargado = pickle.load(file)
        return modelo_cargado
    except Exception as e:
        raise RuntimeError(f"No se pudo cargar el modelo: {str(e)}")


def predecir_diabetes(data, email, usuario_id):
    user_service = UserService()
    try:
        usuario_id = usuario_id.split(":")[1]
        #VALIDACION DE LA EXISTENCIA DEL USUARIO
        if not user_service.usuario_existe(email):
            return 'ERROR.USUARIO INEXISTENTE', 400

        #VALIDACION DEL DOMINIO DE LOS CAMPOS
        if not data.is_valid():
            return 'ERROR. CUERPO DE LA SOLICITUD INCORRECTO.', 400
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
        modelo = cargar_modelo()
        prediccion = modelo.predict(caracteristicas.reshape(1, -1))[0]
        resultado_prediccion = [prediccion[0], "NO", datetime.now().strftime('%Y-%m-%d %H:%M:%S')]
        
        if prediccion[0] < prediccion[1]:
            resultado_prediccion[0] = prediccion[1]
            resultado_prediccion[1] = "SI"

        response = crear_prediccion({'estadoPrediccion': str(resultado_prediccion[1]), 
                                     'prediction': str(resultado_prediccion[0]), 
                                     'fecha' : resultado_prediccion[2], 
                                     'usuario' : email }, usuario_id)
        return "Correcto funcionamiento", response
    except Exception as e:
        raise RuntimeError(f"Error al hacer la predicción: {str(e)}")


def obtener_predicciones_por_usuario(usuario_id):
    #VALIDAR QUE EL USUARIO EXISTA EN LOS REGISTROS
    user_service = UserService()
    if not user_service.usuario_existe(usuario_id):
        return 'USUARIO INEXISTENTE', 400

    predicciones_usuario = obtener_predicciones(usuario_id)
    return predicciones_usuario, 200

    
def obtener_ultima_prediccion(user_id):
    if user_id is None:
        return 'ID DEL USUARIO INVALIDO O NULO', 400

    user_id = str(user_id.split(':')[1])
    return last_prediction(user_id)
