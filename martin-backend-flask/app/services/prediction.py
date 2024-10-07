from ..db.neo4j import db
from .predition_service import process_data
from .models import ModeloML
from .user import User


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
        print(predict)
        print(error)
        prediction = predict

        # next_id = db.get_next_id()

        db.execute_write(
            """
            CREATE (p:Prediction {
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
                Prediction: $prediction
            })
            """,
            {
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
                "prediction": prediction
            }
        )
        query = """
            MATCH (u:User {email: $email})
            MATCH (p:Prediction {user_email: $email})
            CREATE (u)-[:HAVE {fecha: timestamp()}]->(p)
              """
        parameters = {
            "email": user_email,
        }
        if prediction:
            db.execute_write(query, parameters)
            return prediction
        return 'Error al realizar la prediccion'
        # return Prediction(next_id,
        #                   high_bp, high_chol, bmi, smoker, stroke,
        #                   heart_disease_or_attack, phys_activity, gen_hlth,
        #                   ment_hlth, phys_hlth, age
        #                   )

    @staticmethod
    def get_user_predictions(user_email):
        query = """
        MATCH (u:User)-[:HAVE]->(p:Prediction)
        WHERE u.email = $email
        RETURN p
        """
        parameters = {"email": user_email}
        result, code = db.execute_read(query, parameters)

        predictions = []
        for record in result:
            predictions.append(record['p'].get('Prediction'))

        return predictions
