from app import mongo
from pymongo.errors import PyMongoError

class Modelo:

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