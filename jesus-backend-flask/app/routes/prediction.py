from flask import Blueprint, jsonify, request
from app.models.prediction import Modelo
from app.schema.prediction_schema import validate_prediction_input


prediction_bp = Blueprint('prediction', __name__)

#============================ PREDICCION: POST ============================#
@prediction_bp.route("/guardar/predicciones", methods=["POST"])
def add_prediction():
    try:
        data = request.get_json()
        error = validate_prediction_input(data)
        if data is None:
            return jsonify({"error": "Invalid JSON"}), 400
        if error:
            return jsonify({'error': error}), 400
    
        prediction = Modelo(
            correo=data["correo"],
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
            Age=data["Age"],
        )
        prediction.predict()
        result = prediction.save_predicition()
        return jsonify({
            'message': "Prediction added successfully",
            '_id': str(result.inserted_id),
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
@prediction_bp.route('/prediccion/<user_correo>', methods=['GET'])
def get_prediction(user_correo):
    prediction = Modelo.find_by_email(user_correo)
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
