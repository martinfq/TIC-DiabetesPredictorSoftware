import pickle
from ..config import db
class ModeloML:
    def __init__(self, model_path):
        with open(model_path, 'rb') as file:
            self.model = pickle.load(file)

    def predecir(self, data):
        try:
            resultado = self.model.predict([data['feature']])[0]
            return resultado, None
        except Exception as e:
            return None, str(e)

# models.py


class User:
    def __init__(self, username, email):
        self.username = username
        self.email = email

    @staticmethod
    def create_user(username, email):
        with db.driver.session() as session:
            session.run(
                "CREATE (u:User {username: $username, email: $email})",
                username=username, email=email
            )

    @staticmethod
    def get_user_by_username(username):
        with db.driver.session() as session:
            result = session.run(
                "MATCH (u:User {username: $username}) RETURN u.username AS username, u.email AS email",
                username=username
            )
            record = result.single()
            if record:
                return User(record["username"], record["email"])
            return None
