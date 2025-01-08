from unittest.mock import MagicMock, patch
from pymongo.errors import PyMongoError
from datetime import datetime
from app.services.prediction_services import (
    save_prediction,
    make_prediction,
    clasify_age_group,
    predict_diabetes,
    load_model,
)

# Mock de la base de datos
mock_db = MagicMock()


# GUARDAR PREDICCIÓN: EXITO
def test_save_prediction_success(mocker):
    mocker.patch("app.services.prediction_services.mongo", MagicMock(db=mock_db))
    data = MagicMock(
        user_email="test@example.com",
        HighBp=1,
        HighChol=0,
        BMI=25.5,
        Smoker=0,
        Stroke=0,
        HeartDiseaseorAttack=0,
        PhysActivity=1,
        GenHlth=4,
        MentHlth=2,
        PhysHlth=5,
        Age=35,
    )
    prediction_result = {"prediction_class": 1, "prediction_confidence": 0.85}
    mock_db.prediction.insert_one.return_value = MagicMock(inserted_id="some_id")

    result = save_prediction(data, prediction_result)

    assert result is not None
    mock_db.prediction.insert_one.assert_called_once()


# CREAR PREDICCIÓN: EXITO
def test_make_prediction_success(mocker):
    mock_model = MagicMock()
    mock_scaler = MagicMock()
    mock_scaler.transform.return_value = [[0.1, 0.2, 0.3]]
    mocker.patch("app.services.prediction_services.load_model", return_value=(mock_model, mock_scaler))
    mocker.patch("app.services.prediction_services.predict_diabetes", return_value={
        "prediction_class": 1,
        "prediction_confidence": 0.85,
    })

    data = MagicMock(
        HighBp=1,
        HighChol=0,
        BMI=25.5,
        Smoker=0,
        Stroke=0,
        HeartDiseaseorAttack=0,
        PhysActivity=1,
        GenHlth=4,
        MentHlth=2,
        PhysHlth=5,
        Age=35,
    )

    result = make_prediction(data)

    assert result is not None
    assert result["prediction_class"] == 1
    assert result["prediction_confidence"] == 0.85


# CLASIFICAR EDAD
def test_clasify_age_group():
    assert clasify_age_group(23) == 1
    assert clasify_age_group(35) == 4
    assert clasify_age_group(81) == 13
    assert clasify_age_group(17) is None  


# CARGAR MODELO: EXITO
def test_load_model_success(mocker):
    mock_model = MagicMock()
    mock_scaler = MagicMock()
    mocker.patch("builtins.open", MagicMock())
    mocker.patch("pickle.load", side_effect=[mock_model, mock_scaler])

    result = load_model()

    assert result is not None
    assert result[0] == mock_model
    assert result[1] == mock_scaler


# PREDICT DIABETES: EXITO
def test_predict_diabetes_success(mocker):
    mock_model = MagicMock()
    mock_scaler = MagicMock()
    mock_scaler.transform.return_value = [[0.1, 0.2, 0.3]]
    mock_model.predict.return_value = [[0.2, 0.8]]
    mocker.patch("app.services.prediction_services.np.argmax", return_value=1)

    features = [1, 0, 25.5, 0, 0, 0, 1, 4, 2, 5, 4]

    result = predict_diabetes(mock_model, mock_scaler, features)

    assert result["prediction_class"] == 1
    assert result["prediction_confidence"] == 0.8