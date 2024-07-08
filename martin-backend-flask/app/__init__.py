from flask import Flask
from .routes import prediction_routes, user_routes, testdb
import os


def create_app():
    app = Flask(__name__)
    #app.config.from_object('config.Config')
    app.register_blueprint(testdb.main_blueprint)
    app.register_blueprint(prediction_routes.data_blueprint)
    app.register_blueprint(user_routes.user_blueprint)
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'a_very_secret_key'
    return app
