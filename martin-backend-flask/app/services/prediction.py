from ..db.neo4j import db


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
    def create_prediction(high_bp, high_chol, bmi, smoker, stroke, heart_disease_or_attack, phys_activity, gen_hlth,
                          ment_hlth, phys_hlth, age):

        db.execute_write(
            """
            CREATE (p:Prediction {
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
                Age: $age
            })
            """,
            {
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
                "age": age
            }
        )
        return Prediction(
            high_bp, high_chol, bmi, smoker, stroke,
            heart_disease_or_attack, phys_activity, gen_hlth,
            ment_hlth, phys_hlth, age
        )
