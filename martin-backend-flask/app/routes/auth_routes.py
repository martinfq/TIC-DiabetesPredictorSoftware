from flask import request, jsonify, Blueprint
from flask_restful import Resource
from flask_login import login_user, logout_user, LoginManager
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, JWTManager
from ..services.user import User

login_manager = LoginManager()
jwt = JWTManager()

auth_bp = Blueprint('auth', __name__)


@login_manager.user_loader
def load_user(user_id):
    return User.get_user_by_email(user_id)


class AuthLogin(Resource):
    def post(self):
        email = request.json.get('email', None)
        contraseña = request.json.get('contraseña', None)
        user = User.get_user_by_email(email)

        if user and user.contraseña == contraseña:
            login_user(user)
            access_token = create_access_token(identity={'email': user.email, 'nombre': user.nombre})
            return jsonify(access_token=access_token), 200
        return jsonify({"msg": "Bad email or password"}), 401


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


auth_bp.add_url_rule('/login', view_func=AuthLogin.as_view('login'))
auth_bp.add_url_rule('/logout', view_func=AuthLogout.as_view('logout'))
auth_bp.add_url_rule('/protected', view_func=Protected.as_view('protected'))