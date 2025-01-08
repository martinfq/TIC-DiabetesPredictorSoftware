import pickle
import os
import numpy as np
from app import mongo
from datetime import datetime, timezone
from pymongo.errors import PyMongoError
from app.models.prediction_model import Prediccion

# Rangos de edad y su grupo
age_ranges = [
    (18, 24, 1),
    (25, 29, 2),
    (30, 34, 3),
    (35, 39, 4),
    (40, 44, 5),
    (45, 49, 6),
    (50, 54, 7),
    (55, 59, 8),
    (60, 64, 9),
    (65, 69, 10),
    (70, 74, 11),
    (75, 79, 12),
    (80, float('inf'), 13)
]

#  Clasificacion de la edad por grupos:
def clasify_age_group(edadUser):
    for lower, upper, group in age_ranges:
        if lower <= edadUser <= upper:
            return group
        
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
        HighBp=data["HighBp"],
        HighChol=data["HighChol"],
        BMI=round(data["BMI"], 2),
        Smoker=data["Smoker"],
        Stroke=data["Stroke"],
        HeartDiseaseorAttack=data["HeartDiseaseorAttack"],
        PhysActivity=data["PhysActivity"],
        GenHlth=data["GenHlth"],
        MentHlth=data["MentHlth"],
        PhysHlth=data["PhysHlth"],
        Age=edadUser,
    )

# Funcion que ejecuta la prediccion
def predict_diabetes(modelo, scaler, data):
    try:
        np_features = np.array(data).reshape(1,-1)
        scaled_features = scaler.transform(np_features)
        result_predict = modelo.predict(scaled_features)[0]

        prediction_class = int(np.argmax(result_predict))
        prediction_confidence = round(float(result_predict[prediction_class]),4)
        return {"prediction_class": prediction_class, "prediction_confidence": prediction_confidence}
    except Exception as e:
        print(f"Error al crear la prediccion: {e}")
        return None
    
# Funcion que prepara los datos, carga el modelo y ejecuta la predicción
def make_prediction (data_prediction):
    try:
        features = [
            float(data_prediction.HighBp), 
            float(data_prediction.HighChol), 
            float(round(data_prediction.BMI, 0)), 
            float(data_prediction.Smoker), 
            float(data_prediction.Stroke), 
            float(data_prediction.HeartDiseaseorAttack), 
            float(data_prediction.PhysActivity), 
            float(data_prediction.GenHlth), 
            float(data_prediction.MentHlth), 
            float(data_prediction.PhysHlth), 
            clasify_age_group(data_prediction.Age)
        ]

        model_loaded = load_model()
        model, scaler = model_loaded
        return predict_diabetes(model, scaler, features)
    except Exception as e:
        print(f"Error en el flujo de predicción: {e}")
        raise

# Funcion que almacena la prediccion en la DB
def save_prediction(data, data_prediction_result):
    try:
        current_time = datetime.now(timezone.utc).strftime('%d-%m-%Y, %H:%M:%S')
        prediction_data = {
            'user_email': data.user_email, 
            'HighBp': data.HighBp, 
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
            'class': data_prediction_result["prediction_class"],
            'prediction': data_prediction_result["prediction_confidence"],
            'date': current_time
        }
        prediction_created = mongo.db.prediction.insert_one(prediction_data)
        return prediction_created
    except PyMongoError as e:
        print(f"Error al crear la prediccion: {e}")
        return None