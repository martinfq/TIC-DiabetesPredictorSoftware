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
            modelo = pickle.load(file)
        with open('scalerANN.pkl', 'rb') as file:
            scaler = pickle.load(file)
        return modelo, scaler
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
        predictionAge = categorize_age(data.age)
        caracteristicas = np.array([
            float(data.highBP),
            float(data.highChol),
            float(data.bmi),
            float(data.smoker),
            float(data.stroke),
            float(data.heartDiseaseOrAttack),
            float(data.physActivity),
            float(data.genHlth),
            float(data.mentHlth),
            float(data.physHlth),
            float(predictionAge)
        ])
        modelo, scaler = cargar_modelo()
        caracteristicas_escaladas = scaler.transform(caracteristicas.reshape(1,-1))
        prediccion = modelo.predict(caracteristicas_escaladas)[0]
        print(prediccion)
        resultado_prediccion = [prediccion[0], 0, datetime.now().strftime('%Y-%m-%d %H:%M:%S')]
        
        if prediccion[0] < prediccion[1]:
            resultado_prediccion[0] = prediccion[1]
            resultado_prediccion[1] = 1

        response = crear_prediccion({
            'class': resultado_prediccion[1], 
            'prediction': str(resultado_prediccion[0]), 
            'date': resultado_prediccion[2], 
            'usuario': email, 
            'Stroke': data.stroke,
            'HighBp': data.highBP,
            'HighChol': data.highChol, 
            'BMI': data.bmi, 
            'Smoker': data.smoker,
            'HeartDiseaseorAttack': data.heartDiseaseOrAttack,
            'PhysActivity': data.physActivity, 
            'GenHlth': data.genHlth, 
            'MentHlth': data.mentHlth,
            'PhysHlth': data.physHlth,
            'Age': data.age 
        }, usuario_id);
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

def categorize_age(age):
    ageCategory = 0
    if 18 <= age <= 24:
        ageCategory = 1
    elif 25 <= age <= 29:
        ageCategory = 2
    elif 30 <= age <= 34:
        ageCategory = 3
    elif 35 <= age <= 39:
        ageCategory = 4
    elif 40 <= age <= 44:
        ageCategory = 5
    elif 45 <= age <= 49:
        ageCategory = 6
    elif 50 <= age <= 54:
        ageCategory = 7
    elif 55 <= age <= 59:
        ageCategory = 8
    elif 60 <= age <= 64:
        ageCategory = 9
    elif 65 <= age <= 69:
        ageCategory = 10
    elif 70 <= age <= 74:
        ageCategory = 11
    elif 75 <= age <= 79:
        ageCategory = 12
    elif 80 <= age:
        ageCategory = 13
    return ageCategory