from flask import Blueprint, request, jsonify
from .services import process_data
from .models import User
from .config import db

main_blueprint = Blueprint('main', __name__)


@main_blueprint.route('/model', methods=['POST'])
def index():
    data = request.json
    resultado, error = process_data(data)

    if error:
        return jsonify({'error': error}), 400
    else:
        return jsonify({'resultado': resultado}), 200


@main_blueprint.route('/register', methods=['POST'])
def register_user():
    data = request.get_json()
    username = data['username']
    email = data['email']

    existing_user = User.get_user_by_username(username)
    if existing_user:
        return jsonify({"message": "User already exists"}), 400

    User.create_user(username, email)
    return jsonify({"message": "User created successfully"}), 201


@main_blueprint.route('/user/<username>', methods=['POST'])
def get_user(username):
    user = User.get_user_by_username(username)
    if user:
        return jsonify({"username": user.username, "email": user.email}), 200
    return jsonify({"message": "User not found"}), 404


@main_blueprint.route('/id/<id>', methods=['POST'])
def get_user_by_id(user_id):
    user = User.get_user_by_id(user_id)
    if user:
        return jsonify({"user_id": user.user_id, "username": user.username, "email": user.email}), 200
    return jsonify({"message": "User not found"}), 404


@main_blueprint.route('/test_db', methods=['GET'])
def test_db_connection():
    try:
        with db.driver.session() as session:
            result = session.run("RETURN 'Neo4j connection successful' AS message")
            message = result.single()["message"]
            return jsonify({"message": message}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
