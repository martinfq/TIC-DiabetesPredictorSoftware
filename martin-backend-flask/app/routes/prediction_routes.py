import json

from flask import Blueprint, request
from flask_restful import Resource, Api
from ..services.predition_service import process_data
from .schemas.prediction_schema import PredictionSchema
from marshmallow import ValidationError
from ..services.prediction import Prediction
from flask_jwt_extended import (jwt_required, decode_token)
from flask import jsonify

data_blueprint = Blueprint('data', __name__)
api = Api(data_blueprint)


class DataModel(Resource):
    def post(self):
        data = request.json
        resultado, error = process_data(data)
        if error:
            return {'error': error}, 400
        else:
            return resultado, 200


class RegisterPrediction(Resource):
    @jwt_required()
    def post(self):
        # Obtener el token JWT y decodificarlo
        token = request.headers.get('Authorization').split()[1]
        decoded_token = decode_token(token)
        user_email_from_token = decoded_token.get(
            'sub')

        # Obtener los datos del cuerpo de la solicitud
        json_data = request.get_json()
        prediction_schema = PredictionSchema()

        try:
            # Validar y cargar los datos
            data = prediction_schema.load(json_data)
        except ValidationError as err:
            return {"errors": err.messages}, 400

        prediction = Prediction.create_prediction(
            user_email=user_email_from_token,  # Usar el email decodificado del token
            high_bp=data['HighBp'],
            high_chol=data['HighChol'],
            bmi=data['BMI'],
            smoker=data['Smoker'],
            stroke=data['Stroke'],
            heart_disease_or_attack=data['HeartDiseaseorAttack'],
            phys_activity=data['PhysActivity'],
            gen_hlth=data['GenHlth'],
            ment_hlth=data['MentHlth'],
            phys_hlth=data['PhysHlth'],
        )

        # Retornar la predicción creada
        return {"prediction": prediction}, 201


class GetPredictionByEmail(Resource):
    @jwt_required()
    def get(self):
        token = request.headers.get('Authorization').split()[1]
        decoded_token = decode_token(token)
        email_from_token = decoded_token.get(
            'sub')
        prediction = Prediction.get_user_predictions(email_from_token)
        if prediction:
            return prediction, 200
        else:
            return {"message": "User not found or error occurred"}, 404


class GetLastPrediction(Resource):
    @jwt_required()
    def get(self):
        token = request.headers.get('Authorization').split()[1]
        decoded_token = decode_token(token)
        email_from_token = decoded_token.get(
            'sub')
        prediction = Prediction.get_last_prediction(email_from_token)
        if prediction:
            return prediction, 200
        else:
            return {"message": "User not found or error occurred"}, 404


api.add_resource(DataModel, '/model')
api.add_resource(RegisterPrediction, '/predict/register')
api.add_resource(GetPredictionByEmail, '/predict/')
api.add_resource(GetLastPrediction, '/last-predict/')
