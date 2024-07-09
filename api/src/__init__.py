from flask import Flask
from routes import users_routes, predictions_routes

app = Flask(__name__)


def init_app():
    app.register_blueprint(users_routes.app, url_prefix='/usuarios')
    app.register_blueprint(predictions_routes.app, url_prefix='/predicciones')
    
    return app