from flask import Blueprint, request
from flask_restful import Resource, Api
from ..services.predition_service import process_data

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


api.add_resource(DataModel, '/model')
