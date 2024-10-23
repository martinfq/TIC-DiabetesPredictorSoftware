from flask import Blueprint, request, jsonify
import hashlib, uuid, jwt
from services.prediction_service import predecir_diabetes, cargar_modelo, obtener_predicciones_por_usuario
from models.caracteristicas_prediccion import CaracteristicasPrediccion

app = Blueprint('predictions_blueprint', __name__)

@app.route('/predict/register', methods=['POST'])
def crear_prediccion():
    #LECTURA DE DATOS DESDE EL QUERY
    token_session = request.headers.get('Authorization')
    data = request.json 
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
        age = data.get('Age', 5)
    )

    #VALIDACION DEL TOKEN DE SESSION
    if not token_session:
        return jsonify({'ERROR': 'TOKEN FALTANTE'}), 401

    try:
        email = jwt.decode(token_session.split(" ")[1], "passPrueba", algorithms=['HS256']).get("email")
        usuario_id = jwt.decode(token_session.split(" ")[1], "passPrueba", algorithms=['HS256']).get("id")
        resultado = predecir_diabetes(caracteristicas, email, usuario_id)
        if resultado[1] != 200:
            return jsonify({'mensaje': resultado[0]}), resultado[1]

        return jsonify({'mensaje': 'PREDICCION REGISTRADA CON EXITO'}), 200
    except jwt.InvalidTokenError:
        return jsonify({'ERROR': 'TOKEN INVALIDO'}), 400



@app.route('/usuario', methods=['GET'])
def obtener_predicciones():
    #LECTURA DE DATOS DESDE EL QUERY
    token_session = request.headers.get('Authorization')
    if not token_session:
        return jsonify({'ERROR': 'TOKEN FALTANTE'}), 401

    try:
        email = jwt.decode(token_session.split(" ")[1], "passPrueba", algorithms=['HS256']).get("email")    
        predicciones = obtener_predicciones_por_usuario(email)
        if predicciones[1] != 200:
            return jsonify({'mensaje': predicciones[0]}), resultado[1]

        return jsonify({'Predicciones': predicciones[0]}), 200
    except jwt.InvalidTokenError:
        return jsonify({'ERROR': 'TOKEN INVALIDO'}), 400
