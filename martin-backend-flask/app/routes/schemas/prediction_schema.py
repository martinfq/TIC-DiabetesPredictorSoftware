from marshmallow import Schema, fields, validate


class PredictionSchema(Schema):
    HighBp = fields.Float(required=True)
    HighChol = fields.Float(required=True)
    BMI = fields.Float(required=True)
    Smoker = fields.Float(required=True)
    Stroke = fields.Float(required=True)
    HeartDiseaseorAttack = fields.Float(required=True)
    PhysActivity = fields.Float(required=True)
    GenHlth = fields.Float(required=True)
    MentHlth = fields.Float(required=True)
    PhysHlth = fields.Float(required=True)

