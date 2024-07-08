from neo4j import GraphDatabase, exceptions
from .config import Config


class Database:
    def __init__(self, uri, user, password):
        try:
            self.driver = GraphDatabase.driver(uri, auth=(user, password))
        except exceptions.ServiceUnavailable as e:
            print(f"Error: Could not connect to the database service. Details: {e}")
        except exceptions.AuthError as e:
            print(f"Error: Authentication failed. Details: {e}")
        except Exception as e:
            print(f"Error: An unexpected error occurred. Details: {e}")

    def close(self):
        try:
            self.driver.close()
        except Exception as e:
            print(f"Error: Failed to close the database connection. Details: {e}")

    def execute_read(self, query, parameters=None):
        try:
            with self.driver.session() as session:
                result = session.run(query, parameters)
                return result.data()
        except exceptions.ClientError as e:
            print(f"Error: Client error while executing read query. Details: {e}")
        except exceptions.DatabaseError as e:
            print(f"Error: Database error while executing read query. Details: {e}")
        except exceptions.TransientError as e:
            print(f"Error: Transient error while executing read query. Details: {e}")
        except Exception as e:
            print(f"Error: An unexpected error occurred while executing read query. Details: {e}")
            return None

    def execute_write(self, query, parameters=None):
        try:
            with self.driver.session() as session:
                session.run(query, parameters)
        except exceptions.ClientError as e:
            print(f"Error: Client error while executing write query. Details: {e}")
        except exceptions.DatabaseError as e:
            print(f"Error: Database error while executing write query. Details: {e}")
        except exceptions.TransientError as e:
            print(f"Error: Transient error while executing write query. Details: {e}")
        except Exception as e:
            print(f"Error: An unexpected error occurred while executing write query. Details: {e}")


# Inicializa la conexión
db = Database(Config.NEO4J_URI,Config.NEO4J_USER, Config.NEO4J_PASSWORD)
