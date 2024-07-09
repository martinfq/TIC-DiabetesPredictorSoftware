from flask import Blueprint, request, jsonify
from database.redis_connection import redis_connection
import hashlib, uuid, jwt
from services.prediction_service import predecir_diabetes, cargar_modelo
from models.caracteristicas_prediccion import CaracteristicasPrediccion
from services.prediction_service import obtener_predicciones_por_usuario
from services.user_service import usuario_existe


app = Blueprint('predictions_blueprint', __name__)


@app.route('/crear', methods=['POST'])
def crear_prediccion():
    #LECTURA DE DATOS DESDE EL QUERY
    token_session = request.headers.get('Authorization')
    data = request.json 
    highBP = data.get('HighBP')
    highChol = data.get('HighChol')
    bmi = data.get('BMI')
    smoker = data.get('Smoker')
    stroke = data.get('Stroke')
    heartDiseaseOrAttack = data.get('HeartDiseaseOrAttack')
    physActivity = data.get('PhysActivity')
    genHlth = data.get('GenHlth')
    mentHlth = data.get('MentHlth')
    physHlth = data.get('PhysHlth')
    age = data.get('Age')

    #LECTURA DE DATOS DEL TOKEN DE USUARIO
    if not token_session:
        return jsonify({'ERROR': 'TOKEN FALTANTE'}), 401

    try:
        email = jwt.decode(token_session.split(" ")[1], "passPrueba", algorithms=['HS256']).get("email")

        #VALIDAR QUE EL USUARIO EXISTA EN LOS REGISTROS
        if not usuario_existe(email):
            return jsonify({'ERROR': 'USUARIO INEXISTENTE'}), 400

        #VALIDA QUE NINGUNO DE LOS CAMPOS SOLICITADOS SEA NULO
        if(highBP is None or highChol is None or bmi is None or smoker is None or stroke is None or
            heartDiseaseOrAttack is None or physActivity is None or genHlth is None or mentHlth is None or
            physHlth is None or age is None):
            return jsonify({'mensaje': 'CUERPO DE LA SOLICITUD INCORRECTO.'}), 400
        
        #VALIDAR DOMINIO DE LOS CAMPOS
        

        #Contruir Objeto de Caracteristicas de prediccion
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


        modelo = cargar_modelo()
        resultado = predecir_diabetes(modelo, caracteristicas)

        #GENERA LA PREDICCION
        if resultado is None:
            return jsonify({'mensaje': 'ERROR AL GENERAR LA PREDICCION'}), 400

        #CONSTRUCCION DEL NUEVO OBJETO
        prediccion = {'estadoPrediccion': str(resultado), 'probabilidad': "%", 'usuario' : email }

        prediccion_id = str(uuid.uuid4())
        
        connection = redis_connection()
        connection.hset(f"prediccion:{prediccion_id}", mapping=prediccion) #CREACION DE PREDICCIONES
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
        usuario_id = jwt.decode(token_session.split(" ")[1], "passPrueba", algorithms=['HS256']).get("email")
        #VALIDAR QUE EL USUARIO EXISTA EN LOS REGISTROS
        connection = redis_connection()
        print(usuario_id)
        if connection.sismember("USUARIOS", usuario_id) == 0:
            return jsonify({'ERROR': 'USUARIO INEXISTENTE'}), 400

        connection.connection_pool.disconnect()
        predicciones = obtener_predicciones_por_usuario(usuario_id)

        return jsonify({'Predicciones': predicciones}), 200
    except jwt.InvalidTokenError:
        return jsonify({'ERROR': 'TOKEN INVALIDO'}), 400
