from unittest.mock import MagicMock
from app.schema.user_schema import (
    validate_login,
    validate_user,
    validate_email,
    validate_password,
    validate_nombreApellido,
    validate_genero,
    validate_fecha,
)

# Mock de la base de datos
mock_db = MagicMock()
mock_db.user.find_one.side_effect = lambda query: {"email": "existing_user@example.com", "password": "hashed_password"} if query.get("email") == "existing_user@example.com" else None


# LOGIN: EXITO
def test_validate_login_success(mocker):
    mocker.patch("app.schema.user_schema.mongo", MagicMock(db=mock_db))
    data = {"email": "existing_user@example.com", "password": "ValidPassword123!"}
    mocker.patch("app.schema.user_schema.check_password_hash", return_value=True)

    errors = validate_login(data)
    assert errors is None


# LOGIN: FALLO
def test_validate_login_missing_fields(mocker):
    mocker.patch("app.schema.user_schema.mongo", MagicMock(db=mock_db))
    data = {"password": "ValidPassword123!"}
    mocker.patch("app.schema.user_schema.check_password_hash", return_value=True)

    errors = validate_login(data)
    assert len(errors) == 1
    assert "El campo email es requerido." in errors


# LOGIN: FALLO
def test_validate_login_email_not_registered(mocker):
    mocker.patch("app.schema.user_schema.mongo", MagicMock(db=mock_db))
    data = {"email": "not_registered@example.com", "password": "ValidPassword123!"}

    errors = validate_login(data)
    assert "El usuario 'not_registered@example.com' no está registrado." in errors


# USUARIO: EXITO
def test_validate_user_success(mocker):
    mocker.patch("app.schema.user_schema.mongo", MagicMock(db=mock_db))
    data = {
        "name": "Jesus",
        "last_name": "Gonzalez",
        "email": "new_user@example.com",
        "password": "ValidPassword123!",
        "gender": "Masculino",
        "birthday": "1990-01-01",
    }

    errors = validate_user(data)
    assert errors is None


# USUARIO: FALLO
def test_validate_user_missing_fields(mocker):
    mocker.patch("app.schema.user_schema.mongo", MagicMock(db=mock_db))
    data = {
        "last_name": "Gonzalez",
        "email": "new_user@example.com",
        "password": "ValidPassword123!",
        "gender": "Masculino",
        "birthday": "1990-01-01",
    }

    errors = validate_user(data)
    assert len(errors) == 1
    assert "El campo name es requerido." in errors


# USUARIO: FALLO
def test_validate_user_email_already_registered(mocker):
    mocker.patch("app.schema.user_schema.mongo", MagicMock(db=mock_db))
    data = {
        "name": "Jesus",
        "last_name": "Gonzalez",
        "email": "existing_user@example.com",
        "password": "ValidPassword123!",
        "gender": "Masculino",
        "birthday": "1990-01-01",
    }

    errors = validate_user(data)
    assert "El correo 'existing_user@example.com' ya está registrado." in errors


# CAMPOS
def test_validate_email():
    assert validate_email("valid@example.com")
    assert not validate_email("invalid-email")


def test_validate_password():
    assert validate_password("StrongPass123@")
    assert not validate_password("weakpass")


def test_validate_nombreApellido():
    assert validate_nombreApellido("Jesus Gonzalez")
    assert not validate_nombreApellido("123Invalid")


def test_validate_genero():
    assert validate_genero("Masculino")
    assert not validate_genero("Other")


def test_validate_fecha():
    assert validate_fecha("1990-01-01")
    assert not validate_fecha("01-01-1990")