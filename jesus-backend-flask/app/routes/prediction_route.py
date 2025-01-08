import jwt
from flask import Blueprint, jsonify, request, abort
from app.models.prediction_model import Prediccion
from app.schema.prediction_schema import validate_prediction_input
from app.models.user_model import User
from app.services.prediction_services import save_prediction, create_prediction_object, make_prediction


prediction_bp = Blueprint('prediction', __name__)

#============================ PREDICCION: POST ============================# /predict/create
@prediction_bp.route("/predict/register", methods=["POST"])
def add_prediction():
    try:
        # leo el token
        access_token = request.headers.get('Authorization')
        # validacion del token 
        if not access_token:
            abort(401, description='Token faltante')
        # Info del usuario
        user_email = jwt.decode(access_token.split(" ")[1], "passPrueba", algorithms=['HS256'])['email']
        # Extraigo la edad del usuario
        edadUser = User.find_by_email(user_email)['age']
        data = request.get_json()
        # Validar datos de entrada
        error = validate_prediction_input(data)
        print(data)
        if error:
            abort(400, description=error)
            
        # Creo el objeto para la prediccion
        data_prediction = create_prediction_object(data, user_email, edadUser)

        # Realizo la prediccion, obtengo su valor y el de la clase
        data_prediction_result = make_prediction(data_prediction)

        # Guardo la prediccion en la base de datos
        save_prediction(data_prediction, data_prediction_result)

        return jsonify({
            'message': "Prediction added successfully",
            'usuario': user_email,
            'edad': edadUser,
            'prediccion_clase': data_prediction_result["prediction_class"],
            'prediccion': data_prediction_result["prediction_confidence"]
        }), 201
    except jwt.ExpiredSignatureError:
        abort(401, description='Token expirado')
    except jwt.InvalidTokenError:
        abort(401, description='Token inválido')
    except Exception as e:
        abort(500, description=f'error {str(e)}')

#============================ PREDICCION: GET BY EMAIL ============================#
@prediction_bp.route('/predict/', methods=['GET'])
def get_prediction():
    
    # leo el token
    access_token = request.headers.get('Authorization')
    # validacion del token 
    if not access_token:
        return jsonify({'error': 'Token faltante'}), 401
    
    try:
        # info del usuario
        user_email = jwt.decode(access_token.split(" ")[1], "passPrueba", algorithms=['HS256'])['email']
        # Predicciones
        prediction = Prediccion.find_by_email(user_email)
        return jsonify(prediction), 200
    except Exception as e:
        return jsonify({'error': f'Ocurrió un error: {str(e)}'}), 500
    
#============================ PREDICCION: GET LAST BY EMAIL ============================#
@prediction_bp.route('/last-predict/', methods=['GET'])
def get_last_prediction():
    
    # leo el token
    access_token = request.headers.get('Authorization')
    # validacion del token 
    if not access_token:
        return jsonify({'error': 'Token faltante'}), 401
    
    try:
        # info del usuario
        user_email = jwt.decode(access_token.split(" ")[1], "passPrueba", algorithms=['HS256'])['email']

        # ultima prediccion
        prediction = Prediccion.find_last_by_email(user_email)
        if prediction:
            return jsonify(prediction), 200
        else:
            return jsonify({'resultado': 'No se encontró ninguna predicción para este usuario'}), 200
    except Exception as e:
        # Manejo de errores adicionales
        return jsonify({'error': f'Ocurrió un error: {str(e)}'}), 500