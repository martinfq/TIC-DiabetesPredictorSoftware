from ..db.neo4j import db


class User:
    def __init__(self, username, email, nombre, apellido, contraseña, fecha_nacimiento=None, genero=None):
        self.username = username
        self.email = email
        self.nombre = nombre
        self.apellido = apellido
        self.contraseña = contraseña
        self.fecha_nacimiento = fecha_nacimiento
        self.genero = genero

    @staticmethod
    def validate_fields(**kwargs):
        required_fields = ['username', 'email', 'nombre', 'apellido', 'contraseña']
        for field in required_fields:
            if not kwargs.get(field):
                raise ValueError(f"El campo '{field}' es obligatorio.")

    @staticmethod
    def create_user(username, email, nombre, apellido, contraseña, fecha_nacimiento=None, genero=None):
        User.validate_fields(username=username, email=email, nombre=nombre, apellido=apellido, contraseña=contraseña)

        db.execute_write(
            """
            CREATE (u:User {
                username: $username, 
                email: $email,
                nombre: $nombre,
                apellido: $apellido,
                contraseña: $contraseña,
                fecha_nacimiento: $fecha_nacimiento,
                genero: $genero
            })
            """,
            {
                "username": username,
                "email": email,
                "nombre": nombre,
                "apellido": apellido,
                "contraseña": contraseña,
                "fecha_nacimiento": fecha_nacimiento,
                "genero": genero
            }
        )
        return User(username, email, nombre, apellido, contraseña, fecha_nacimiento, genero)

    @staticmethod
    def get_user(query, value):
        result = db.execute_read(
            f"""
            MATCH (u:User {{{query}: $value}}) 
            RETURN u.username AS username, u.email AS email, u.nombre AS nombre, u.apellido AS apellido, 
                   u.contraseña AS contraseña, u.fecha_nacimiento AS fecha_nacimiento, u.genero AS genero
            """,
            {"value": value}
        )
        if result:
            record = result[0]
            return User(record["username"], record["email"], record["nombre"], record["apellido"],
                        record["contraseña"], record["fecha_nacimiento"], record["genero"])
        return None

    @staticmethod
    def get_user_by_username(username):
        return User.get_user("username", username)

    @staticmethod
    def get_user_by_email(email):
        return User.get_user("email", email)
