from ..db.neo4j import db
from .predition_service import process_data
from .models import ModeloML


class Prediction:
    next_id = 1

    def __init__(self, id, high_bp, high_chol, bmi, smoker, stroke, heart_disease_or_attack, phys_activity, gen_hlth,
                 ment_hlth, phys_hlth, age):
        self.id = id
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
                          ment_hlth, phys_hlth, age):
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
        age = float(age)

        # Crear la lista de floats
        data = [
            high_bp, high_chol, bmi, smoker, stroke, heart_disease_or_attack, phys_activity, gen_hlth, ment_hlth,
            phys_hlth, age
        ]
        modelo = ModeloML('model.pkl')
        predict, error = modelo.predecir2(data)
        prediction = float(predict[0])

        next_id = db.get_next_id()

        db.execute_write(
            """
            CREATE (p:Prediction {
                user_email:$user_email,
                id: $id,
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
                Prediction: $prediction
            })
            """,
            {
                "user_email": user_email,
                "id": next_id,
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
                "age": age,
                "prediction": prediction
            }
        )
        db.execute_write(
            """
            MATCH (u:User {email: 1})
            MATCH (p:Prediccion {user_email: 1}), (c2:Calificación {id_calificación: 2})
            CREATE (u)-[:CALIFICÓ {fecha: timestamp()}]->(c1)
            CREATE (u)-[:CALIFICÓ {fecha: timestamp()}]->(c2)
            """
        )
        return Prediction(next_id,
                          high_bp, high_chol, bmi, smoker, stroke,
                          heart_disease_or_attack, phys_activity, gen_hlth,
                          ment_hlth, phys_hlth, age
                          )
