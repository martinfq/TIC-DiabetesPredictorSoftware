import pickle
from .config import db
import uuid
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
    def __init__(self, user_id, username, email):
        self.user_id = user_id
        self.username = username
        self.email = email

    @staticmethod
    def create_user(username, email):
        user_id = str(uuid.uuid4())
        with db.driver.session() as session:
            session.run(
                "CREATE (u:User {user_id: $user_id, username: $username, email: $email})",
                user_id=user_id, username=username, email=email
            )
        return User(user_id, username, email)

    @staticmethod
    def get_user_by_username(username):
        with db.driver.session() as session:
            result = session.run(
                "MATCH (u:User {username: $username}) RETURN u.user_id AS user_id, u.username AS username, u.email AS email",
                username=username
            )
            record = result.single()
            if record:
                return User(record["user_id"], record["username"], record["email"])
            return None

    @staticmethod
    def get_user_by_id(user_id):
        with db.driver.session() as session:
            result = session.run(
                "MATCH (u:User {user_id: $user_id}) RETURN u.user_id AS user_id, u.username AS username, u.email AS email",
                user_id=user_id
            )
            record = result.single()
            if record:
                return User(record["user_id"], record["username"], record["email"])
            return None
