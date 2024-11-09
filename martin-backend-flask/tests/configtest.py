# tests/conftest.py
import pytest
from ..app import create_app
from neo4j import GraphDatabase
from datetime import timedelta
import os


@pytest.fixture(scope="session")
def app():
    """Crea una instancia de la aplicación Flask en modo de pruebas"""
    app = create_app()
    app.config["TESTING"] = True
    app.config["SECRET_KEY"] = "test_secret_key"
    app.config["JWT_SECRET_KEY"] = "test_jwt_secret_key"
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=5)  # Expira en 5 minutos para pruebas
    return app


@pytest.fixture(scope="session")
def client(app):
    """Cliente de pruebas de Flask para hacer peticiones a la API"""
    return app.test_client()


@pytest.fixture(scope="session")
def neo4j_db():
    """Configura la conexión a una base de datos Neo4j en modo de pruebas"""
    uri = os.getenv("NEO4J_TEST_URI", "bolt://localhost:7687")
    user = os.getenv("NEO4J_TEST_USER", "neo4j")
    password = os.getenv("NEO4J_TEST_PASSWORD", "esteban98")

    driver = GraphDatabase.driver(uri, auth=(user, password))

    with driver.session() as session:
        # Limpia la base de datos antes de iniciar las pruebas
        session.run("MATCH (n) DETACH DELETE n")

    yield driver  # Proporciona el driver para las pruebas

    with driver.session() as session:
        # Limpia la base de datos después de todas las pruebas
        session.run("MATCH (n) DETACH DELETE n")

    driver.close()


@pytest.fixture
def jwt_token(client):
    """Genera un token JWT para pruebas de endpoints protegidos"""
    response = client.post("/login", json={"username": "test_user", "password": "test_password"})
    assert response.status_code == 200
    return response.json["access_token"]
