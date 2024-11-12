import json

from ..db.neo4j import db
from .predition_service import process_data
from .models import ModeloML
from .user import User
import datetime
import uuid


class Prediction:

    def __init__(self, high_bp, high_chol, bmi, smoker, stroke, heart_disease_or_attack, phys_activity, gen_hlth,
                 ment_hlth, phys_hlth, age):
        self.HighBp = high_bp
        self.HighChol = high_chol
        self.BMI = bmi
        self.Smoker = smoker
        self.Stroke = stroke
        self.HeartDiseaseorAttack = heart_disease_or_attack
        self.PhysActivity = phys_activity
        self.GenHlth = gen_hlth
        self.MentHlth = ment_hlth
        self.PhysHlth = phys_hlth
        self.Age = age

    @staticmethod
    def create_prediction(user_email, high_bp, high_chol, bmi, smoker, stroke, heart_disease_or_attack, phys_activity,
                          gen_hlth,
                          ment_hlth, phys_hlth):
        # Convertir todos los parámetros a floats
        high_bp = float(high_bp)
        high_chol = float(high_chol)
        bmi = float(bmi)
        smoker = float(smoker)
        stroke = float(stroke)
        heart_disease_or_attack = float(heart_disease_or_attack)
        phys_activity = float(phys_activity)
        gen_hlth = float(gen_hlth)
        ment_hlth = float(ment_hlth)
        phys_hlth = float(phys_hlth)

        #Obtener age
        user_age = float(User.get_user_age(user_email))

        data = [
            high_bp, high_chol, bmi, smoker, stroke, heart_disease_or_attack, phys_activity, gen_hlth, ment_hlth,
            phys_hlth, user_age
        ]
        modelo = ModeloML('modelANN.pkl', 'scalerANN.pkl')
        predict, error = modelo.predecir_ann(data)
        class_0 = predict[0]
        class_1 = predict[1]

        if class_0 > class_1:
            prediction = class_0
            class_value = 0
        else:
            prediction = class_1
            class_value = 1

        pred_id = str(uuid.uuid4())

        db.execute_write(
            """
            CREATE (p:Prediction {
                id:$id,
                user_email:$user_email,
                HighBp: $high_bp,
                HighChol: $high_chol,
                BMI: $bmi,
                Smoker: $smoker,
                Stroke: $stroke,
                HeartDiseaseorAttack: $heart_disease_or_attack,
                PhysActivity: $phys_activity,
                GenHlth: $gen_hlth,
                MentHlth: $ment_hlth,
                PhysHlth: $phys_hlth,
                Age: $age,
                class_0: $class_0,
                class_1: $class_1,
                prediction:$prediction,
                class:$class
            })
            """,
            {
                "id": pred_id,
                "user_email": user_email,
                "high_bp": high_bp,
                "high_chol": high_chol,
                "bmi": bmi,
                "smoker": smoker,
                "stroke": stroke,
                "heart_disease_or_attack": heart_disease_or_attack,
                "phys_activity": phys_activity,
                "gen_hlth": gen_hlth,
                "ment_hlth": ment_hlth,
                "phys_hlth": phys_hlth,
                "age": user_age,
                "class_0": class_0,
                "class_1": class_1,
                "prediction": prediction,
                "class": class_value
            }
        )
        query = """
            MATCH (u:User {email: $email})
            MATCH (p:Prediction {id: $id})
            CREATE (u)-[:HAVE {fecha: timestamp()}]->(p)
              """
        parameters = {
            "email": user_email,
            "id": pred_id
        }
        if predict:
            db.execute_write(query, parameters)
            return prediction
        return 'Error al realizar la prediccion'

    @staticmethod
    def get_user_predictions(user_email):
        query = """
        MATCH (u:User)-[h:HAVE]->(p:Prediction)
        WHERE u.email = $email
        RETURN p,h.fecha
        ORDER BY h.fecha DESC
        """
        parameters = {"email": user_email}
        result, code = db.execute_read(query, parameters)
        predictions = []
        for record in result:
            dt = datetime.datetime.fromtimestamp(record["h.fecha"] / 1000)
            fecha = dt.date()
            hora = dt.strftime("%H:%M")
            data = record["p"]
            data["date"] = fecha.isoformat()
            data["time"] = hora
            predictions.append(data)

        return predictions

    @staticmethod
    def get_last_prediction(user_email):
        query = """
                MATCH (u:User)-[h:HAVE]->(p:Prediction)
                WHERE u.email = $email
                RETURN p,h.fecha
                ORDER BY h.fecha DESC
                LIMIT 1
                """
        parameters = {"email": user_email}
        result, code = db.execute_read(query, parameters)

        data = {
            "prediction": result[0]["p"]["prediction"],
            "date": result[0]["h.fecha"]
        }
        return data
