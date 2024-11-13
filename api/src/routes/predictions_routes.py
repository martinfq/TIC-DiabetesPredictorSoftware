from flask import Blueprint, request, jsonify
import hashlib, uuid, jwt
from services.prediction_service import predecir_diabetes, cargar_modelo, obtener_predicciones_por_usuario, obtener_ultima_prediccion
from services.user_service import *
from models.caracteristicas_prediccion import CaracteristicasPrediccion

app = Blueprint('predictions_blueprint', __name__)

@app.route('/predict/register', methods=['POST'])
def crear_prediccion():
    #LECTURA DE DATOS DESDE EL QUERY
    token_session = request.headers.get('Authorization')
    data = request.json 

    #VALIDACION DEL TOKEN DE SESSION
    if not token_session:
        return jsonify({'ERROR': 'TOKEN FALTANTE'}), 401

    try:
        email = jwt.decode(token_session.split(" ")[1], "passPrueba", algorithms=['HS256']).get("email")
        usuario_id = jwt.decode(token_session.split(" ")[1], "passPrueba", algorithms=['HS256']).get("id")
        user_service = UserService()
        user_data = user_service.datos_usuario(usuario_id)[0]

        caracteristicas = CaracteristicasPrediccion(
            highBP = data.get('HighBp'),
            highChol = data.get('HighChol'),
            bmi = data.get('BMI'),
            smoker = data.get('Smoker'),
            stroke = data.get('Stroke'),
            heartDiseaseOrAttack = data.get('HeartDiseaseorAttack'),
            physActivity = data.get('PhysActivity'),
            genHlth = data.get('GenHlth'),
            mentHlth = data.get('MentHlth'),
            physHlth = data.get('PhysHlth'),
            age = int(user_data['age'])
        )
        resultado = predecir_diabetes(caracteristicas, email, usuario_id)
        if resultado[1] != 200:
            return jsonify({'mensaje': resultado[0]}), resultado[1]

        return jsonify({'mensaje': 'PREDICCION REGISTRADA CON EXITO'}), 200
    except jwt.InvalidTokenError:
        return jsonify({'ERROR': 'TOKEN INVALIDO'}), 400



@app.route('/predict/', methods=['GET'])
def obtener_predicciones():
    token_session = request.headers.get('Authorization')
    if not token_session:
        return jsonify({'ERROR': 'TOKEN FALTANTE'}), 401

    try:
        email = jwt.decode(token_session.split(" ")[1], "passPrueba", algorithms=['HS256']).get("email")    
        predicciones = obtener_predicciones_por_usuario(email)
        if predicciones[1] != 200:
            return jsonify({'mensaje': predicciones[0]}), resultado[1]

        return jsonify(predicciones[0]), 200
    except jwt.InvalidTokenError:
        return jsonify({'ERROR': 'TOKEN INVALIDO'}), 400



@app.route('/last-predict/', methods=['GET'])
def last_prediction():
    token_session = request.headers.get('Authorization')
    if not token_session:
        return jsonify({'ERROR': 'TOKEN FALTANTE'}), 401

    try:
        user_id = jwt.decode(token_session.split(" ")[1], "passPrueba", algorithms=['HS256']).get("id")     
        last_prediction = obtener_ultima_prediccion(user_id)

        return jsonify(last_prediction), 200
    except jwt.InvalidTokenError:
        return jsonify({'ERROR': 'TOKEN INVALIDO'}), 400
