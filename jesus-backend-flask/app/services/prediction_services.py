import pickle
import os
from app import mongo
from pymongo.errors import PyMongoError

def load_model():
    try:
        model_path = os.path.join(os.path.dirname(__file__), 'model.pkl')
        with open(model_path, 'rb') as file:
            model = pickle.load(file)
        return model
    except Exception as e:
        print(f"Error al cargar el modelo: {e}")
        return None

def predict_diabetes(modelo, data):
    features = [data.BP, data.Chol, data.BMI, data.Smoker, data.Stroke, data.HDA, data.PA, data.GH, data.MH, data.PH, data.Age]
    data.rPrediccion = modelo.predict([features])[0]

def save_predicition(data):
    try:
        prediction_data = {
            'correo': data.correo, 
            'BP': data.BP, 
            'Chol': data.Chol, 
            'BMI': data.BMI,
            'Smoker': data.Smoker, 
            'Stroke': data.Stroke, 
            'HDA': data.HDA, 
            'PA': data.PA, 
            'GH': data.GH, 
            'MH': data.MH, 
            'PH': data.PH,
            'Age': data.Age,
            'rPrediccion': data.rPrediccion
        }
        prediction_created = mongo.db.prediction.insert_one(prediction_data)
        return prediction_created
    except PyMongoError as e:
        print(f"Error al crear la prediccion: {e}")
        return None