from flask import Blueprint, request, jsonify
from database.redisConnection import redis_connection
import hashlib, uuid
from services.PredictionService import predecirDiabetes, cargarModelo
from models.CaracteristicasPrediccionModelo import CaracteristicasPrediccion
from services.PredictionService import obtenerPrediccionesPorUsuario


app = Blueprint('predictions_blueprint', __name__)


@app.route('/crear', methods=['POST'])
def crearPrediccion():
    #LECTURA DE DATOS DESDE EL QUERY
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
    usuario_id = data.get('usuario_id')

    #VALIDAR QUE EL USUARIO EXISTA EN LOS REGISTROS
    connection = redis_connection()
    if connection.sismember("USUARIOS", usuario_id) == 0:
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


    modelo = cargarModelo()

    resultado = predecirDiabetes(modelo, caracteristicas)

    #GENERA LA PREDICCION
    if resultado is None:
        return jsonify({'mensaje': 'ERROR AL GENERAR LA PREDICCION'}), 400

    #connection = redis_connection()

    #CONSTRUCCION DEL NUEVO OBJETO
    prediccion = {'estadoPrediccion': resultado, 'probabilidad': "%", 'usuario' : usuario_id }

    prediccion_id = str(uuid.uuid4())

    connection.hset(f"prediccion:{prediccion_id}", mapping=prediccion) #CREACION DE PREDICCIONES
    connection.sadd("PREDICCIONES", prediccion_id) #Modificar por sets inversos

    connection.connection_pool.disconnect()
    
    return jsonify({'mensaje': 'PREDICCION REGISTRADA CON EXITO', 'prediccion': prediccion}), 200



@app.route('/usuario', methods=['GET'])
def obtenerPredicciones():
    #LECTURA DE DATOS DESDE EL QUERY
    usuario_id = request.args.get('id', default=None, type=str)

    print('F')
    #VALIDAR QUE EL USUARIO EXISTA EN LOS REGISTROS
    connection = redis_connection()
    if connection.sismember("USUARIOS", usuario_id) == 0:
        return jsonify({'ERROR': 'USUARIO INEXISTENTE'}), 400

    connection.connection_pool.disconnect()
    print('c')
    predicciones = obtenerPrediccionesPorUsuario(usuario_id)
    print('A')
    return jsonify({'Predicciones': predicciones}), 200
