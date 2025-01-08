from flask import Flask, jsonify
from flask_pymongo import PyMongo
from app.config import Config
from flask_cors import CORS

# Inicializacion de la app y config
mongo = PyMongo()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    mongo.init_app(app)
    CORS(app)
    # Blueprints
    from app.routes.user_route import user_bp
    from app.routes.prediction_route import prediction_bp

    app.register_blueprint(user_bp)
    app.register_blueprint(prediction_bp)

    #errores
    @app.errorhandler(401)
    def unauthorized_error(e):
        return jsonify({"message": str(e)}), 401
    
    @app.errorhandler(500)
    def internal_server_error(e):
        return jsonify({"message": f'error {str(e)}'}), 500
    
    return app