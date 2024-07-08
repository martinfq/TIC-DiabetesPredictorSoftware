from flask import Flask
from flask_pymongo import PyMongo
from app.config import Config

# Inicializacion de la app y config
mongo = PyMongo()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    mongo.init_app(app)

    # Blueprints
    from app.routes.user import user_bp
    from app.routes.prediction import prediction_bp

    app.register_blueprint(user_bp)
    app.register_blueprint(prediction_bp)
    
    return app