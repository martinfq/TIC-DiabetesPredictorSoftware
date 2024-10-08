import json

from flask import Blueprint, request, jsonify
from flask_restful import Resource, Api
from marshmallow import ValidationError
from ..services.user import User
from .schemas.user_schema import UserSchema

from flask_jwt_extended import (jwt_required)

user_blueprint = Blueprint('user', __name__)
api = Api(user_blueprint)

user_schema = UserSchema()
user_update_schema = UserSchema(partial=True)


class Users(Resource):
    @jwt_required()
    def get(self):
        try:
            users = User.get_all_users()
            return jsonify([user.__dict__ for user in users])
        except Exception as e:
            return {'error': str(e)}, 500


class RegisterUser(Resource):
    def post(self):
        json_data = request.get_json()

        try:
            data = user_schema.load(json_data)
        except ValidationError as err:
            return {"errors": err.messages}, 400

        existing_user = User.get_user_by_email(data['email'])
        if existing_user:
            return {"message": "User already exists"}, 409

        user = User.create_user(
            email=data['email'],
            name=data['name'],
            last_name=data['last_name'],
            password=data['password'],
            birthday=data.get('birthday'),
            gender=data.get('gender')
        )
        return {"email": user.email, "message": "User created successfully"}, 201


class GetUserByEmail(Resource):
    def get(self):
        email = request.args.get('email')
        user_info = User.get_user_by_email(email)
        if user_info:
            return json.loads(user_info), 200
        else:
            return {"message": "User not found or error occurred"}, 404


class UpdateUser(Resource):
    def put(self, username):
        try:
            # Valida y deserializa la entrada
            args = user_update_schema.load(request.json)
        except ValidationError as err:
            return err.messages, 400

        try:
            updated_user = User.update_user(
                args.get('email'),
                args.get('name'),
                args.get('last_name'),
                args.get('password'),
                args.get('birthday'),
                args.get('gender')
            )
            if updated_user:
                return jsonify(updated_user.__dict__)
            else:
                return {'message': 'User not found'}, 404
        except Exception as e:
            return {'error': str(e)}, 500


api.add_resource(Users, '/users')
api.add_resource(UpdateUser, '/users/<string:username>')
api.add_resource(RegisterUser, '/user/register')
api.add_resource(GetUserByEmail, '/user/')
