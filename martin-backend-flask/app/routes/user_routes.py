from flask import Blueprint, request, jsonify
from flask_restful import Resource, Api
from marshmallow import ValidationError
from ..models.user import User
from ..schemas.user_schema import UserSchema

user_blueprint = Blueprint('user', __name__)
api = Api(user_blueprint)


class RegisterUser(Resource):
    def post(self):
        json_data = request.get_json()
        user_schema = UserSchema()
        try:
            data = user_schema.load(json_data)
        except ValidationError as err:
            return {"errors": err.messages}, 400

        existing_user = User.get_user_by_email(data['email'])
        if existing_user:
            return {"message": "User already exists"}, 400

        user = User.create_user(
            username=data['username'],
            email=data['email'],
            nombre=data['nombre'],
            apellido=data['apellido'],
            contraseña=data['contraseña'],
            fecha_nacimiento=data.get('fecha_nacimiento'),
            genero=data.get('genero')
        )
        return {"email": user.email, "message": "User created successfully"}, 201


class GetUser(Resource):
    def get(self, username):
        user = User.get_user_by_username(username)
        if user:
            return {"username": user.username, "email": user.email}, 200
        else:
            return {"message": "User not found or error occurred"}, 404


class GetUserByEmail(Resource):
    def get(self, email):
        user = User.get_user_by_email(email)
        if user:
            return {"username": user.username, "email": user.email}, 200
        else:
            return {"message": "User not found or error occurred"}, 404


api.add_resource(RegisterUser, '/register')
api.add_resource(GetUser, '/user/<username>')
api.add_resource(GetUserByEmail, '/user/email/<email>')
