from app.schema.prediction_schema import validate_prediction_input


# PREDICCIONL: EXITO
def test_validate_prediction_input_success():
    data = {
        'HighBp': 1,
        'HighChol': 0,
        'BMI': 22.5,
        'Smoker': 1,
        'Stroke': 0,
        'HeartDiseaseorAttack': 1,
        'PhysActivity': 0,
        'GenHlth': 3,
        'MentHlth': 10,
        'PhysHlth': 5
    }
    errors = validate_prediction_input(data)
    assert errors is None


# PREDICCIONL: FALLO
def test_validate_prediction_input_missing_fields():
    data = {
        'HighBp': 1,
        'BMI': 22.5
    }
    errors = validate_prediction_input(data)
    assert len(errors) == 8  # Faltan 8 campos
    assert "El campo HighChol es requerido." in errors


# PREDICCIONL: FALLO
def test_validate_prediction_input_invalid_HighBp():
    data = {
        'HighBp': 2,  # Valor inválido
        'HighChol': 1,
        'BMI': 22.5,
        'Smoker': 1,
        'Stroke': 0,
        'HeartDiseaseorAttack': 1,
        'PhysActivity': 1,
        'GenHlth': 3,
        'MentHlth': 10,
        'PhysHlth': 5
    }
    errors = validate_prediction_input(data)
    assert "El BP debe ser un número entre 0 y 1." in errors


# PREDICCIONL: FALLO
def test_validate_prediction_input_invalid_BMI():
    data = {
        'HighBp': 1,
        'HighChol': 1,
        'BMI': 5.0,  # Menor al mínimo permitido
        'Smoker': 1,
        'Stroke': 0,
        'HeartDiseaseorAttack': 1,
        'PhysActivity': 1,
        'GenHlth': 3,
        'MentHlth': 10,
        'PhysHlth': 5
    }
    errors = validate_prediction_input(data)
    assert "El BMI debe ser un número mayor a 10." in errors


# PREDICCIONL: FALLO
def test_validate_prediction_input_invalid_GenHlth():
    data = {
        'HighBp': 1,
        'HighChol': 1,
        'BMI': 22.5,
        'Smoker': 1,
        'Stroke': 0,
        'HeartDiseaseorAttack': 1,
        'PhysActivity': 1,
        'GenHlth': 6,  # Fuera del rango permitido
        'MentHlth': 10,
        'PhysHlth': 5
    }
    errors = validate_prediction_input(data)
    assert "El GenHlth debe ser un número entre 1 y 5." in errors


# PREDICCIONL: FALLO
def test_validate_prediction_input_invalid_MentHlth():
    data = {
        'HighBp': 1,
        'HighChol': 1,
        'BMI': 22.5,
        'Smoker': 1,
        'Stroke': 0,
        'HeartDiseaseorAttack': 1,
        'PhysActivity': 1,
        'GenHlth': 3,
        'MentHlth': 35,  # Fuera del rango permitido
        'PhysHlth': 5
    }
    errors = validate_prediction_input(data)
    assert "El MentHlth debe ser un número entre 0 y 30." in errors


# PREDICCIONL: FALLO
def test_validate_prediction_input_invalid_PhysHlth():
    data = {
        'HighBp': 1,
        'HighChol': 1,
        'BMI': 22.5,
        'Smoker': 1,
        'Stroke': 0,
        'HeartDiseaseorAttack': 1,
        'PhysActivity': 1,
        'GenHlth': 3,
        'MentHlth': 10,
        'PhysHlth': 31  # Fuera del rango permitido
    }
    errors = validate_prediction_input(data)
    assert "El PhysHlth debe ser un número entre 0 y 1." in errors
