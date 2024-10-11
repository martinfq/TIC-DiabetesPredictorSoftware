from flask import Blueprint, request, jsonify
from database.redis_connection import redis_connection
import hashlib, uuid, jwt
from services.prediction_service import predecir_diabetes, cargar_modelo, obtener_predicciones_por_usuario
from models.caracteristicas_prediccion import CaracteristicasPrediccion
from services.user_service import UserService


app = Blueprint('predictions_blueprint', __name__)
user_service = UserService()

@app.route('/crear', methods=['POST'])
def crear_prediccion():
    #LECTURA DE DATOS DESDE EL QUERY
    token_session = request.headers.get('Authorization')
    data = request.json 
    caracteristicas = CaracteristicasPrediccion(
        highBP = data.get('HighBP'),
        highChol = data.get('HighChol'),
        bmi = data.get('BMI'),
        smoker = data.get('Smoker'),
        stroke = data.get('Stroke'),
        heartDiseaseOrAttack = data.get('HeartDiseaseOrAttack'),
        physActivity = data.get('PhysActivity'),
        genHlth = data.get('GenHlth'),
        mentHlth = data.get('MentHlth'),
        physHlth = data.get('PhysHlth'),
        age = data.get('Age')
    )

    #VALIDACION DEL TOKEN DE SESSION
    if not token_session:
        return jsonify({'ERROR': 'TOKEN FALTANTE'}), 401

    try:
        email = jwt.decode(token_session.split(" ")[1], "passPrueba", algorithms=['HS256']).get("email")

        #VALIDACION DE LA EXISTENCIA DEL USUARIO
        if not user_service.usuario_existe(email):
            return jsonify({'ERROR': 'USUARIO INEXISTENTE'}), 400

        #VALIDACION DEL DOMINIO DE LOS CAMPOS
        if not caracteristicas.is_valid():
            return jsonify({'mensaje': 'CUERPO DE LA SOLICITUD INCORRECTO.'}), 400
        
        #CARGA DEL MODELO Y GENERACION DE LA PREDICCION
        modelo = cargar_modelo()
        resultado = predecir_diabetes(modelo, caracteristicas)
      
        if resultado is None:
            return jsonify({'mensaje': 'ERROR AL GENERAR LA PREDICCION'}), 400

        prediccion = {'estadoPrediccion': str(resultado), 'probabilidad': "%", 'usuario' : email }

        prediccion_id = str(uuid.uuid4())       
        connection = redis_connection()
        connection.hmset(f"prediccion:{prediccion_id}", prediccion) #CREACION DE PREDICCIONES
        connection.sadd("PREDICCIONES", prediccion_id) #Modificar por sets inversos
        connection.connection_pool.disconnect()
        
        return jsonify({'mensaje': 'PREDICCION REGISTRADA CON EXITO', 'prediccion': prediccion}), 200
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
        
        #VALIDAR QUE EL USUARIO EXISTA EN LOS REGISTROS
        if not user_service.usuario_existe(email):
            return jsonify({'ERROR': 'USUARIO INEXISTENTE'}), 400

        predicciones = obtener_predicciones_por_usuario(email)
        return jsonify({'Predicciones': predicciones}), 200

    except jwt.InvalidTokenError:
        return jsonify({'ERROR': 'TOKEN INVALIDO'}), 400
