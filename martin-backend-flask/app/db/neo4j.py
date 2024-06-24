from neo4j import GraphDatabase
from ..config import Config


class Database:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def execute_read(self, query, parameters=None):
        with self.driver.session() as session:
            result = session.run(query, parameters)
            return result.data()  # Devuelve todos los registros como una lista de diccionarios

    def execute_write(self, query, parameters=None):
        with self.driver.session() as session:
            session.run(query, parameters)


# Inicializa la conexión
db = Database(Config.NEO4J_URI,Config.NEO4J_USER, Config.NEO4J_PASSWORD)
