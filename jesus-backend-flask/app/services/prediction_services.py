import pickle
import os
import numpy as np
from app import mongo
from datetime import datetime, timezone
from pymongo.errors import PyMongoError
from app.models.prediction_model import Prediccion

# Funcion encargada de cargar el Modelo Predictivo y el Scaler
def load_model():
    try:
        model_path = os.path.join(os.path.dirname(__file__), 'modelANN.pkl')
        model_scaler_path = os.path.join(os.path.dirname(__file__), 'scalerANN.pkl')
        with open(model_path, 'rb') as file:
            model = pickle.load(file)
        with open(model_scaler_path, 'rb') as file:
            scaler = pickle.load(file)
        return model, scaler
    except Exception as e:
        print(f"Error al cargar el modelo: {e}")
        return None
    
# Funcion que define el objeto Prediccion
def create_prediction_object(data, user_email, edadUser):
    return Prediccion(
        user_email=user_email,
        HighBP=data["HighBP"],
        HighChol=data["HighChol"],
        BMI=data["BMI"],
        Smoker=data["Smoker"],
        Stroke=data["Stroke"],
        HeartDiseaseorAttack=data["HeartDiseaseorAttack"],
        PhysActivity=data["PhysActivity"],
        GenHlth=data["GenHlth"],
        MentHlth=data["MentHlth"],
        PhysHlth=data["PhysHlth"],
        Age=edadUser,
    )

# Funcion que llama al modelo y a la funcion que ejecuta la prediccion
def make_prediction (data_prediction):
    features = [
        float(data_prediction.HighBP), 
        float(data_prediction.HighChol), 
        float(data_prediction.BMI), 
        float(data_prediction.Smoker), 
        float(data_prediction.Stroke), 
        float(data_prediction.HeartDiseaseorAttack), 
        float(data_prediction.PhysActivity), 
        float(data_prediction.GenHlth), 
        float(data_prediction.MentHlth), 
        float(data_prediction.PhysHlth), 
        data_prediction.Age
    ]

    model_loaded = load_model()
    model, scaler = model_loaded
    return predict_diabetes(model, scaler, features)

# Funcion que ejecuta la prediccion
def predict_diabetes(modelo, scaler, data):
    try:
        np_features = np.array(data)
        features_scaler = scaler.transform(np_features.reshape(1,-1))
        result_predict = modelo.predict(features_scaler)[0][1]
        return round(float(result_predict),4)
    except Exception as e:
        print(f"Error al crear la prediccion: {e}")
        return None

# Funcion que almacena la prediccion en la DB
def save_prediction(data):
    try:
        current_time = datetime.now(timezone.utc)
        prediction_data = {
            'user_email': data.user_email, 
            'HighBP': data.HighBP, 
            'HighChol': data.HighChol, 
            'BMI': data.BMI,
            'Smoker': data.Smoker, 
            'Stroke': data.Stroke, 
            'HeartDiseaseorAttack': data.HeartDiseaseorAttack, 
            'PhysActivity': data.PhysActivity, 
            'GenHlth': data.GenHlth, 
            'MentHlth': data.MentHlth, 
            'PhysHlth': data.PhysHlth,
            'Age': data.Age,
            'rPrediccion': data.rPrediccion,
            'timestamp': current_time
        }
        prediction_created = mongo.db.prediction.insert_one(prediction_data)
        return prediction_created
    except PyMongoError as e:
        print(f"Error al crear la prediccion: {e}")
        return None