from ..db.neo4j import db


class User:
    def __init__(self, email, name, last_name, password, birthday=None, gender=None,
                 is_authenticated=None, is_active=None, is_anonymous=None):
        self.email = email
        self.name = name
        self.last_name = last_name
        self.password = password
        self.birthday = birthday
        self.gender = gender
        self.is_authenticated = is_authenticated
        self.is_active = is_active
        self.is_anonymous = is_anonymous

    @staticmethod
    def create_user(email, name, last_name, password, birthday=None, gender=None):
        db.execute_write(
            """
            CREATE (u:User {
                email: $email,
                name: $name,
                last_name: $last_name,
                password: $password,
                birthday: $birthday,
                gender: $gender,
                is_authenticated: $is_authenticated,
                is_active:$is_active,
                is_anonymous:$is_anonymous
            })
            """,
            {
                "email": email,
                "name": name,
                "last_name": last_name,
                "password": password,
                "birthday": birthday,
                "gender": gender,
                "is_authenticated": False,
                "is_active":True,
                "is_anonymous": False
            }
        )
        return User(email, name, last_name, password, birthday, gender)

    def get_user(query, value):
        try:
            result, error = db.execute_read(
                f"""
                       MATCH (u:User {{{query}: $value}}) 
                       RETURN u.email AS email, u.name AS name, u.last_name AS last_name, 
                              u.password AS password, u.birthday AS birthday, u.gender AS gender
                       """,
                {"value": value}
            )
            if result:
                record = result[0]
                return User(record["email"], record["name"], record["last_name"],
                            record["password"], record["birthday"], record["gender"])
            return None
        except Exception as e:
            print(f"Error al obtener el usuario: {e}")
            return None

    @staticmethod
    def get_user_by_email(email):
        return User.get_user("email", email)

    @staticmethod
    def get_all_users():
        try:
            results, error = db.execute_read(
                """
                MATCH (u:User)
                RETURN u.email AS email, u.name AS name, u.last_name AS last_name, 
                       u.password AS password, u.birthday AS birthday, u.gender AS gender
                """
            )
            users = []
            for record in results:
                users.append(User(
                    record["email"], record["name"], record["last_name"],
                    record["password"], record["birthday"], record["gender"]
                ))
            return users
        except Exception as e:
            print(f"Error al obtener todos los usuarios: {e}")
            return []

    @staticmethod
    def update_user(email, new_name, new_last_name, new_password, new_birthday=None,
                    new_gender=None):
        try:
            db.execute_write(
                """
                MATCH (u:User {email: $email})
                SET u.name = $new_name,
                    u.last_name = $new_last_name,
                    u.password = $new_password,
                    u.birthday = $new_birthday,
                    u.gender = $new_gender
                """,
                {
                    "name": new_name,
                    "new_last_name": new_last_name,
                    "new_password": new_password,
                    "new_birthday": new_birthday,
                    "new_gender": new_gender
                }
            )
            return User.get_user_by_email(email)
        except Exception as e:
            print(f"Error al actualizar el usuario: {e}")
            return None
