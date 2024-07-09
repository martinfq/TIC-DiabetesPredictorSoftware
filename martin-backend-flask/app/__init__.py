from flask import Flask
from .routes import prediction_routes, user_routes, testdb, auth_routes
import os
from flask_login import LoginManager
from flask_jwt_extended import JWTManager
def create_app():
    app = Flask(__name__)
    #app.config.from_object('config.Config')
    app.register_blueprint(testdb.main_blueprint)
    app.register_blueprint(prediction_routes.data_blueprint)
    app.register_blueprint(user_routes.user_blueprint)
    app.register_blueprint(auth_routes.auth_bp)

    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'a_very_secret_key'
    app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'

    login_manager = LoginManager()
    login_manager.init_app(app)

    jwt = JWTManager(app)
    return app
