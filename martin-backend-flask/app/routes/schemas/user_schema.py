from marshmallow import Schema, fields, validate


class UserSchema(Schema):
    email = fields.Email(required=True)
    nombre = fields.Str(required=True, validate=validate.Length(min=1))
    apellido = fields.Str(required=True, validate=validate.Length(min=1))
    contraseña = fields.Str(required=True, validate=validate.Length(min=6))
    fecha_nacimiento = fields.Date(required=False)
    genero = fields.Str(required=False,
                        validate=validate.OneOf(['male', 'female', 'other']))  # Ejemplo de validación de género


# user_schema = UserSchema()
