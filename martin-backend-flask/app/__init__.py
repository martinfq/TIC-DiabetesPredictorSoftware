from flask import Flask
from .views import main_blueprint
from .routes import prediction_routes,user_routes

def create_app():
    app = Flask(__name__)
    #app.config.from_object('config.Config')
    app.register_blueprint(main_blueprint)
    app.register_blueprint(prediction_routes.data_blueprint)
    app.register_blueprint(user_routes.user_blueprint)
    return app
