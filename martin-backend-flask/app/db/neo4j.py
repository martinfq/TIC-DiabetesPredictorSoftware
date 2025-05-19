from neo4j import GraphDatabase, exceptions
from .config import Config
from flask import jsonify


class Database:
    def __init__(self, uri, user, password):
        try:
            self.driver = GraphDatabase.driver(uri, auth=(user, password))
        except exceptions.ServiceUnavailable as e:
            self.handle_error("Could not connect to the database service.", e, 503)
        except exceptions.AuthError as e:
            self.handle_error("Authentication failed.", e, 401)
        except Exception as e:
            self.handle_error("An unexpected error occurred.", e, 500)

    def handle_error(self, message, exception, status_code):
        print(f"Error: {message} Details: {exception}")
        self.error_response = jsonify({"error": message, "details": str(exception)}), status_code

    def close(self):
        try:
            self.driver.close()
        except Exception as e:
            print(f"Error: Failed to close the database connection. Details: {e}")

    def execute_read(self, query, parameters=None):
        try:
            with self.driver.session() as session:
                result = session.run(query, parameters)
                return result.data(), 200
        except exceptions.ClientError as e:
            return self.handle_error("Client error while executing read query.", e, 400)
        except exceptions.DatabaseError as e:
            return self.handle_error("Database error while executing read query.", e, 500)
        except exceptions.TransientError as e:
            return self.handle_error("Transient error while executing read query.", e, 503)
        except Exception as e:
            return self.handle_error("An unexpected error occurred while executing read query.", e, 500)

    def execute_write(self, query, parameters=None):
        try:
            with self.driver.session() as session:
                session.run(query, parameters)
                return jsonify({"message": "Write query executed successfully."}), 200
        except exceptions.ClientError as e:
            return self.handle_error("Client error while executing write query.", e, 400)
        except exceptions.DatabaseError as e:
            return self.handle_error("Database error while executing write query.", e, 500)
        except exceptions.TransientError as e:
            return self.handle_error("Transient error while executing write query.", e, 503)
        except Exception as e:
            return self.handle_error("An unexpected error occurred while executing write query.", e, 500)

    def get_next_id(self):
        try:
            with self.driver.session() as session:
                query = """MERGE (c:Counter {name: 'prediction_id'}) "
                                     "ON CREATE SET c.value = 0 "
                                     "ON MATCH SET c.value = c.value + 1 "
                                     "RETURN c.value"""
                result = session.run(query)
                return result.single()[0]
        except exceptions.ClientError as e:
            print(f"Error: Client error while getting next ID. Details: {e}")
        except exceptions.DatabaseError as e:
            print(f"Error: Database error while getting next ID. Details: {e}")
        except exceptions.TransientError as e:
            print(f"Error: Transient error while getting next ID. Details: {e}")
        except Exception as e:
            print(f"Error: An unexpected error occurred while getting next ID. Details: {e}")
            return None


# Inicializa la conexión
db = Database(Config.NEO4J_URI, Config.NEO4J_USER, Config.NEO4J_PASSWORD)
