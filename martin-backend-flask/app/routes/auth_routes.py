from flask import request, jsonify, Blueprint
from flask_restful import Resource
from marshmallow import ValidationError
from flask_login import logout_user, LoginManager
from flask_jwt_extended import (jwt_required, get_jwt_identity,
                                JWTManager, verify_jwt_in_request, get_jwt)
from .schemas.login_schema import LoginSchema
from ..services.user import User
from ..services.auth import Auth, UserNotFoundError
from ..services.login_manager import login_manager

jwt = JWTManager()
login_schema = LoginSchema()
auth_bp = Blueprint('auth', __name__)


@login_manager.user_loader
def load_user(user_id):
    return User.get_user_by_email(user_id)


@login_manager.request_loader
def load_user_from_request(request):
    try:
        verify_jwt_in_request()
        jwt_data = get_jwt()
        user_email = jwt_data['sub']['email']
        return User.get_user_by_email(user_email)
    except Exception as e:
        print(f"Error loading user from request: {e}")
        return None


class AuthLogin(Resource):
    def post(self):
        json_data = request.get_json()
        try:
            data = login_schema.load(json_data)
        except ValidationError as err:
            return {"errors": err.messages}, 400
        try:
            access_token = Auth.login(
                email=data['email'],
                password=data['password']
            )
        except UserNotFoundError as e:
            return jsonify({"msg": str(e)}), 404  # Usuario no encontrado
        except ValueError as e:
            return jsonify({"msg": str(e)}), 401  # Error de autenticación

        return jsonify(access_token=access_token), 200


class AuthLogout(Resource):
    @jwt_required()
    def post(self):
        logout_user()
        return jsonify({"msg": "Logged out"}), 200


class Protected(Resource):
    @jwt_required()
    def get(self):
        identity = get_jwt_identity()
        return jsonify(logged_in_as=identity), 200


class VerifyToken(Resource):
    @jwt_required()
    def get(self):
        current_user = get_jwt_identity()
        return jsonify(valid=True, user_id=current_user), 200


auth_bp.add_url_rule('/login', view_func=AuthLogin.as_view('login'))
auth_bp.add_url_rule('/logout', view_func=AuthLogout.as_view('logout'))
auth_bp.add_url_rule('/protected', view_func=Protected.as_view('protected'))
auth_bp.add_url_rule('/verify-token', view_func=Protected.as_view('verify-token'))
