from marshmallow import Schema, fields, validate


class UserSchema(Schema):
    email = fields.Email(required=True)
    name = fields.Str(required=True, validate=validate.Length(min=1))
    last_name = fields.Str(required=True, validate=validate.Length(min=1))
    password = fields.Str(required=True, validate=validate.Length(min=6))
    birthday = fields.Date(required=True)
    gender = fields.Str(required=True,
                        validate=validate.OneOf(['M', 'F']))

# user_schema = UserSchema()
