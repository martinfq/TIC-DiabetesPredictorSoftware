from flask import Blueprint, request, jsonify
from ..models.models import User

user_blueprint = Blueprint('user', __name__)


@user_blueprint.route('/register', methods=['POST'])
def register_user():
    data = request.get_json()
    username = data['username']
    email = data['email']

    existing_user = User.get_user_by_email(email)
    if existing_user:
        return jsonify({"message": "User already exists"}), 400

    user = User.create_user(username, email)
    return jsonify({"email": user.email, "message": "User created successfully"}), 201


@user_blueprint.route('/user/<username>', methods=['GET'])
def get_user(username):
    user = User.get_user_by_username(username)
    if user:
        return jsonify({"username": user.username, "email": user.email}), 200
    return jsonify({"message": "User not found"}), 404


@user_blueprint.route('/user/email/<email>', methods=['GET'])
def get_user_by_email(email):
    user = User.get_user_by_email(email)
    if user:
        return jsonify({"username": user.username, "email": user.email}), 200
    return jsonify({"message": "User not found"}), 404
