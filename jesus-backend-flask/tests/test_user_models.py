from unittest.mock import MagicMock
from app.models.user_model import User

# Mock de la base de datos
mock_db = MagicMock()

# ENCONTRAR POR EMAIL: EXITO
def test_find_by_email_success(mocker):
    mocker.patch("app.models.user_model.mongo", MagicMock(db=mock_db))
    mock_db.user.find_one.return_value = {
        "_id": 1, "name": "John", "last_name": "Doe", "email": "john@example.com", "birthday": "1990-01-01", "gender": "Male", "password": "password123"
    }
    
    result = User.find_by_email("john@example.com")
    
    assert result is not None
    assert result["_id"] == "1"
    assert result["email"] == "john@example.com"


# ENCONTRAR POR EMAIL: FALLO
def test_find_by_email_not_found(mocker):
    mocker.patch("app.models.user_model.mongo", MagicMock(db=mock_db))
    mock_db.user.find_one.return_value = None
    
    result = User.find_by_email("nonexistent@example.com")
    
    assert result is None