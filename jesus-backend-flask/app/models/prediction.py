import pickle
import os
from app import mongo
from pymongo.errors import PyMongoError


class Modelo:
    model = None

    @classmethod
    def load_model(cls):
        if cls.model is None:
            model_path = os.path.join(os.path.dirname(__file__), 'model.pkl')
            with open(model_path, 'rb') as file:
                cls.model = pickle.load(file)

    def __init__(self, correo, BP, Chol, BMI, Smoker, Stroke, HDA, PA, GH, MH, PH, Age):
        self.correo = correo
        self.BP = BP
        self.Chol = Chol
        self.BMI = BMI
        self.Smoker = Smoker
        self.Stroke = Stroke
        self.HDA = HDA
        self.PA = PA
        self.GH = GH
        self.MH = MH
        self.PH = PH
        self.Age = Age
        self.rPrediccion = None

    def predict(self):
        Modelo.load_model()
        features = [self.BP, self.Chol, self.BMI, self.Smoker, self.Stroke, self.HDA, self.PA, self.GH, self.MH, self.PH, self.Age]
        self.rPrediccion = Modelo.model.predict([features])[0]
    
    def save_predicition(self):
        try:
            prediction_data = {
                'correo': self.correo, 
                'BP': self.BP, 
                'Chol': self.Chol, 
                'BMI': self.BMI,
                'Smoker': self.Smoker, 
                'Stroke': self.Stroke, 
                'HDA': self.HDA, 
                'PA': self.PA, 
                'GH': self.GH, 
                'MH': self.MH, 
                'PH': self.PH,
                'Age': self.Age,
                'rPrediccion': self.rPrediccion
            }
            prediction_created = mongo.db.prediction.insert_one(prediction_data)
            return prediction_created
        except PyMongoError as e:
            print(f"Error al crear la prediccion: {e}")
            return None
        
    @staticmethod
    def find_all():
        try:
            prediction_list = []
            for prediction in mongo.db.prediction.find():
                prediction["_id"] = str(prediction["_id"])
                prediction_list.append(prediction)
            return prediction_list
        except PyMongoError as e:
            print(f"Error al obtener las predicciones: {e}")
            return None
    
    @staticmethod
    def find_by_email(correo):
        try:
            predictionRecords = []
            for prediction in mongo.db.prediction.find({"correo": correo}):
                prediction["_id"] = str(prediction["_id"])
                predictionRecords.append(prediction)
            return predictionRecords
        except PyMongoError as e:
            print(f"Error al obtener la prediccion: {e}")
            return None
        
    @staticmethod
    def delete(correo):
        try:
            return mongo.db.prediction.delete_many({"correo": correo})
        except PyMongoError as e:
            print(f"Error al eliminar la prediccion: {e}")
            return False