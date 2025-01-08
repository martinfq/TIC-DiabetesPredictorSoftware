from unittest.mock import MagicMock
from app.services.user_services import save_user, calculateAge
from pymongo.errors import PyMongoError
from datetime import datetime

# Mock de la base de datos
mock_db = MagicMock()


# GUARDAR EL USUARIO: EXITO
def test_save_user_success(mocker):
    mocker.patch("app.services.user_services.mongo", MagicMock(db=mock_db))
    mocker.patch("app.services.user_services.generate_password_hash", return_value="hashed_password")
    
    class UserData:
        def __init__(self, name, last_name, email, password, gender, birthday):
            self.name = name
            self.last_name = last_name
            self.email = email
            self.password = password
            self.gender = gender
            self.birthday = birthday
    
    data = UserData(
        name="John", last_name="Doe", email="john@example.com", password="password123", 
        gender="Male", birthday="1990-01-01"
    )
    
    mock_db.user.insert_one.return_value = MagicMock(inserted_id="some_id")
    result = save_user(data)

    assert result is not None  


# GUARDAR EL USUARIO: FALLO
def test_save_user_fail(mocker):
    mocker.patch("app.services.user_services.mongo", MagicMock(db=mock_db))
    mocker.patch("app.services.user_services.generate_password_hash", return_value="hashed_password")

    class UserData:
        def __init__(self, name, last_name, email, password, gender, birthday):
            self.name = name
            self.last_name = last_name
            self.email = email
            self.password = password
            self.gender = gender
            self.birthday = birthday
    
    data = UserData(
        name="John", last_name="Doe", email="john@example.com", password="password123", 
        gender="Male", birthday="1990-01-01"
    )

    mock_db.user.insert_one.side_effect = PyMongoError("Error de base de datos")
    result = save_user(data)
    
    assert result is None 


# CAULCULO DE EDAD: EXITO
def test_calculate_age_success():
    birth_date = "1990-01-01"
    result = calculateAge(birth_date)
    
    today = datetime.now()
    expected_age = today.year - 1990 - ((today.month, today.day) < (1, 1))
    
    assert result == expected_age 


# CAULCULO DE EDAD: FALLO
def test_calculate_age_invalid_format():
    birth_date = "01-01-1990" 
    result = calculateAge(birth_date) 
    assert result is False