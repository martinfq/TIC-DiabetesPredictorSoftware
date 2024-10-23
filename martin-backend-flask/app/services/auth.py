from .user import User
from flask_login import login_user, logout_user, LoginManager
from flask_jwt_extended import (create_access_token, jwt_required, get_jwt_identity,
                                JWTManager, verify_jwt_in_request, get_jwt)


class Auth:
    def __init__(self, email, password):
        self.email = email
        self.password = password

    @staticmethod
    def login(email, password):
        user = User.get_user_by_email(email)
        if not user:
            raise UserNotFoundError("User not found")
        if user.password != password:
            raise ValueError("Incorrect password")

        login_user(user)
        access_token = create_access_token(identity=user.email)
        return access_token


class UserNotFoundError(Exception):
    """Excepción lanzada cuando no se encuentra el usuario"""
    pass
