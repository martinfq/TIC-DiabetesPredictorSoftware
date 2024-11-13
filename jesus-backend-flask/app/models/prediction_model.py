from app import mongo
from pymongo import DESCENDING
from pymongo.errors import PyMongoError

class Prediccion:
    def __init__(self, user_email, HighBp, HighChol, BMI, Smoker, Stroke, HeartDiseaseorAttack, PhysActivity, GenHlth, MentHlth, PhysHlth, Age):
        self.user_email = user_email
        self.HighBp = HighBp
        self.HighChol = HighChol
        self.BMI = BMI
        self.Smoker = Smoker
        self.Stroke = Stroke
        self.HeartDiseaseorAttack = HeartDiseaseorAttack
        self.PhysActivity = PhysActivity
        self.GenHlth = GenHlth
        self.MentHlth = MentHlth
        self.PhysHlth = PhysHlth
        self.Age = Age
        self.prediction = None
        
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
    def find_by_email(user_email):
        try:
            predictionRecords = []
            for prediction in mongo.db.prediction.find({"user_email": user_email}):
                prediction["_id"] = str(prediction["_id"])
                predictionRecords.append(prediction)
            return predictionRecords
        except PyMongoError as e:
            print(f"Error al obtener la prediccion: {e}")
            return None
        
    @staticmethod
    def find_last_by_email(user_email):
        try:
            prediction = mongo.db.prediction.find_one({"user_email": user_email}, sort=[("_id", DESCENDING)])
            if prediction:
                prediction["_id"] = str(prediction["_id"])
            return prediction
        except PyMongoError as e:
            print(f"Error al obtener la prediccion: {e}")
            return None
        
    @staticmethod
    def delete(user_email):
        try:
            return mongo.db.prediction.delete_many({"user_email": user_email})
        except PyMongoError as e:
            print(f"Error al eliminar la prediccion: {e}")
            return False