from flask import Blueprint, request, jsonify
from .services import process_data

main_blueprint = Blueprint('main', __name__)

@main_blueprint.route('/', methods=['POST'])
def index():
    data = request.json
    resultado, error = process_data(data)

    if error:
        return jsonify({'error': error}), 400
    else:
        return jsonify({'resultado': resultado}), 200
