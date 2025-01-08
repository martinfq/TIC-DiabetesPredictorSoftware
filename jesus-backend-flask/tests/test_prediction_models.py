from unittest.mock import patch, MagicMock
from app.models.prediction_model import Prediccion
from pymongo.errors import PyMongoError

# Mock de la base de datos
mock_db = MagicMock()

# ENCONTRAR PREDICCIONES POR CORREO: EXITO
def test_find_by_email_success(mocker):
    mocker.patch("app.models.prediction_model.mongo", MagicMock(db=mock_db))
    mock_db.prediction.find.return_value =[
        {"Age": 25,
        "BMI": 16,
        "GenHlth": 1,
        "HeartDiseaseorAttack": 1,
        "HighBP": 1,
        "HighChol": 0,
        "MentHlth": 1,
        "PhysActivity": 1,
        "PhysHlth": 1,
        "Smoker": 1,
        "Stroke": 0,
        "_id": 1,
        "date": "Wed, 16 Oct 2024 19:04:15 GMT",
        "prediction": 0.6563,
        "user_email": "marceloj@hotmail.com"}
    ]
    
    result = Prediccion.find_by_email("marceloj@hotmail.com")
    print(result)

    assert result[0]["user_email"] == "marceloj@hotmail.com"
    assert result[0]["BMI"] == 16


# ENCONTRAR PREDICCIONES POR CORREO: FALLO
def test_find_by_email_no_results(mocker):
    mocker.patch("app.models.prediction_model.mongo", MagicMock(db=mock_db))
    mock_db.prediction.find.return_value = []
    
    result = Prediccion.find_by_email("nonexistent@example.com")
    
    assert result == []


# ENCONTRAR PREDICCIONES POR CORREO: FALLO
def test_find_by_email_error(mocker):
    mocker.patch("app.models.prediction_model.mongo", MagicMock(db=mock_db))
    mock_db.prediction.find.side_effect = PyMongoError("Database error")
    
    result = Prediccion.find_by_email("test@example.com")
    
    assert result is None


# ENCONTRAR ULTIMA PREDICCION POR CORREO: EXITO
def test_find_last_by_email_success(mocker):
    mocker.patch("app.models.prediction_model.mongo", MagicMock(db=mock_db))
    mock_db.prediction.find_one.return_value = {"_id": 1, "user_email": "test@example.com", "HighBp": 1, "HighChol": 1, "BMI": 28.5}
    
    result = Prediccion.find_last_by_email("test@example.com")

    assert result is not None
    assert result["user_email"] == "test@example.com"
    assert result["HighBp"] == 1


# ENCONTRAR ULTIMA PREDICCION POR CORREO: FALLO
def test_find_last_by_email_no_results(mocker):
    mocker.patch("app.models.prediction_model.mongo", MagicMock(db=mock_db))
    mock_db.prediction.find_one.return_value = None
    
    result = Prediccion.find_last_by_email("nonexistent@example.com")
    
    assert result is None


# ENCONTRAR ULTIMA PREDICCION POR CORREO: FALLO
def test_find_last_by_email_error(mocker):
    mocker.patch("app.models.prediction_model.mongo", MagicMock(db=mock_db))
    mock_db.prediction.find_one.side_effect = PyMongoError("Database error")
    
    result = Prediccion.find_last_by_email("test@example.com")
    
    assert result is None
