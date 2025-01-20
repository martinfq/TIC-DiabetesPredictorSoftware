from flask import Flask
from .routes import prediction_routes, user_routes, testdb, auth_routes
from flask_jwt_extended import JWTManager
from .services.login_manager import login_manager
from datetime import timedelta
from flask_cors import CORS
from dotenv import load_dotenv
import os


def create_app():
    app = Flask(__name__)
    load_dotenv()
    # app.config.from_object('config.Config')
    CORS(app)
    app.register_blueprint(testdb.main_blueprint)
    app.register_blueprint(prediction_routes.data_blueprint)
    app.register_blueprint(user_routes.user_blueprint)
    app.register_blueprint(auth_routes.auth_bp)

    app.config['DEBUG'] = os.environ.get('FLASK_DEBUG')
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'a_very_secret_key'
    app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)

    login_manager.init_app(app)

    jwt = JWTManager(app)
    return app
