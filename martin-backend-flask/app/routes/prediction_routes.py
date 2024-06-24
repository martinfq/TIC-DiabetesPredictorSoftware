from flask import Blueprint, request, jsonify
from ..services import process_data

data_blueprint = Blueprint('data', __name__)


@data_blueprint.route('/model', methods=['POST'])
def index():
    data = request.json
    resultado, error = process_data(data)

    if error:
        return jsonify({'error': error}), 400
    else:
        return jsonify({'resultado': resultado}), 200
