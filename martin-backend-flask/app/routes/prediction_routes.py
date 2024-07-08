from flask import Blueprint, request
from flask_restful import Resource, Api
from ..services.predition_service import process_data
from .schemas.prediction_schema import PredictionSchema
from marshmallow import ValidationError
from ..services.prediction import Prediction
data_blueprint = Blueprint('data', __name__)
api = Api(data_blueprint)


class DataModel(Resource):
    def post(self):
        data = request.json
        resultado, error = process_data(data)

        if error:
            return {'error': error}, 400
        else:
            return {'resultado': resultado}, 200


class RegisterPrediction(Resource):
    def post(self):
        json_data = request.get_json()
        prediction_schema = PredictionSchema()
        try:
            data = prediction_schema.load(json_data)
        except ValidationError as err:
            return {"errors": err.messages}, 400

        Prediction.create_prediction(
            user_email=data['user_email'],
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
            age=data['Age']
        )
        return {"message": "Prediction created successfully"}, 201


api.add_resource(DataModel, '/model')
api.add_resource(RegisterPrediction, '/predict/register')