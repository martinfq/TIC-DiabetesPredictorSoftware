from ..db.neo4j import db


class User:
    def __init__(self, email, nombre, apellido, contraseña, fecha_nacimiento=None, genero=None,
                 is_authenticated=None, is_active=None, is_anonymous=None):
        self.email = email
        self.nombre = nombre
        self.apellido = apellido
        self.contraseña = contraseña
        self.fecha_nacimiento = fecha_nacimiento
        self.genero = genero
        self.is_authenticated = is_authenticated
        self.is_active = is_active
        self.is_anonymous = is_anonymous

    @staticmethod
    def create_user(email, nombre, apellido, contraseña, fecha_nacimiento=None, genero=None):
        db.execute_write(
            """
            CREATE (u:User {
                email: $email,
                nombre: $nombre,
                apellido: $apellido,
                contraseña: $contraseña,
                fecha_nacimiento: $fecha_nacimiento,
                genero: $genero,
                is_authenticated: $is_authenticated,
                is_active:$is_active,
                is_anonymous:$is_anonymous
            })
            """,
            {
                "email": email,
                "nombre": nombre,
                "apellido": apellido,
                "contraseña": contraseña,
                "fecha_nacimiento": fecha_nacimiento,
                "genero": genero,
                "is_authenticated": False,
                "is_active":True,
                "is_anonymous": False
            }
        )
        return User(email, nombre, apellido, contraseña, fecha_nacimiento, genero)

    def get_user(query, value):
        try:
            result, error = db.execute_read(
                f"""
                       MATCH (u:User {{{query}: $value}}) 
                       RETURN u.email AS email, u.nombre AS nombre, u.apellido AS apellido, 
                              u.contraseña AS contraseña, u.fecha_nacimiento AS fecha_nacimiento, u.genero AS genero
                       """,
                {"value": value}
            )
            if result:
                record = result[0]
                return User(record["email"], record["nombre"], record["apellido"],
                            record["contraseña"], record["fecha_nacimiento"], record["genero"])
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
                RETURN u.email AS email, u.nombre AS nombre, u.apellido AS apellido, 
                       u.contraseña AS contraseña, u.fecha_nacimiento AS fecha_nacimiento, u.genero AS genero
                """
            )
            users = []
            for record in results:
                users.append(User(
                    record["email"], record["nombre"], record["apellido"],
                    record["contraseña"], record["fecha_nacimiento"], record["genero"]
                ))
            return users
        except Exception as e:
            print(f"Error al obtener todos los usuarios: {e}")
            return []

    @staticmethod
    def update_user(email, new_nombre, new_apellido, new_contraseña, new_fecha_nacimiento=None,
                    new_genero=None):
        try:
            db.execute_write(
                """
                MATCH (u:User {email: $email})
                SET u.nombre = $new_nombre,
                    u.apellido = $new_apellido,
                    u.contraseña = $new_contraseña,
                    u.fecha_nacimiento = $new_fecha_nacimiento,
                    u.genero = $new_genero
                """,
                {
                    "new_nombre": new_nombre,
                    "new_apellido": new_apellido,
                    "new_contraseña": new_contraseña,
                    "new_fecha_nacimiento": new_fecha_nacimiento,
                    "new_genero": new_genero
                }
            )
            return User.get_user_by_email(email)
        except Exception as e:
            print(f"Error al actualizar el usuario: {e}")
            return None
