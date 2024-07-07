from flask import Flask
from routes import UsersRoutes, PredictionsRoutes

app = Flask(__name__)


def init_app():
    app.register_blueprint(UsersRoutes.app, url_prefix='/usuarios')
    app.register_blueprint(PredictionsRoutes.app, url_prefix='/predicciones')
    
    return app