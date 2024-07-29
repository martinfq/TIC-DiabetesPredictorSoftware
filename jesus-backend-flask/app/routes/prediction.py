import jwt
from flask import Blueprint, jsonify, request
from app.models.prediction import Modelo
from app.schema.prediction_schema import validate_prediction_input
from app.models.user import User


prediction_bp = Blueprint('prediction', __name__)

#============================ PREDICCION: POST ============================#
@prediction_bp.route("/guardar/predicciones", methods=["POST"])
def add_prediction():
    try:
        # leo el token
        token_session = request.headers.get('Authorization')
        # validacion del token 
        if not token_session:
            return jsonify({'error': 'Token faltante'}), 401
        # info del usuario
        correoUser = jwt.decode(token_session.split(" ")[1], "passPrueba", algorithms=['HS256'])['correo']
        edadUser = User.find_by_email(correoUser)['edad']

        data = request.get_json()

        # Validar datos de entrada
        error = validate_prediction_input(data)
        if error:
            return jsonify({'error': error}), 400
    
        prediction = Modelo(
            correo=correoUser,
            BP=data["BP"],
            Chol=data["Chol"],
            BMI=data["BMI"],
            Smoker=data["Smoker"],
            Stroke=data["Stroke"],
            HDA=data["HDA"],
            PA=data["PA"],
            GH=data["GH"],
            MH=data["MH"],
            PH=data["PH"],
            Age=edadUser,
        )

        prediction.predict()
        result = prediction.save_predicition()
        return jsonify({
            'message': "Prediction added successfully",
            '_id': str(result.inserted_id),
            'usuario': correoUser,
            'edad': edadUser,
            'prediccion': prediction.rPrediccion
        }), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

#============================ PREDICCION: GET ALL ============================#
@prediction_bp.route("/predicciones", methods=["GET"])
def get_all_predictions():
    predictions = Modelo.find_all()
    return jsonify(predictions), 200

#============================ PREDICCION: GET BY EMAIL ============================#
@prediction_bp.route('/prediccion/usuario', methods=['GET'])
def get_prediction():
    
    # leo el token
    token_session = request.headers.get('Authorization')
    # validacion del token 
    if not token_session:
        return jsonify({'error': 'Token faltante'}), 401
    # info del usuario
    correoUser = jwt.decode(token_session.split(" ")[1], "passPrueba", algorithms=['HS256'])['correo']

    prediction = Modelo.find_by_email(correoUser)
    return jsonify(prediction), 200
    

#============================ PREDICCION: DELETE ============================#
@prediction_bp.route('/delete_prediction/<user_correo>', methods=['DELETE'])
def delete_user(user_correo):
    prediction = Modelo.find_by_email(user_correo)
    if prediction:
        Modelo.delete(user_correo)
        return jsonify({'message': 'Prediction deleted successfully'}), 200
    else:
        return jsonify({'error': 'Prediction not found'}), 404
