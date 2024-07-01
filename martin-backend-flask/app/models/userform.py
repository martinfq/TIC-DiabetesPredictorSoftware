from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, DateField, SelectField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo


class UserForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=50)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    nombre = StringField('Nombre', validators=[DataRequired(), Length(min=2, max=50)])
    apellido = StringField('Apellido', validators=[DataRequired(), Length(min=2, max=50)])
    contraseña = PasswordField('Contraseña', validators=[DataRequired(), Length(min=6)])
    confirm_contraseña = PasswordField('Confirm Contraseña', validators=[DataRequired(), EqualTo('contraseña',
                                                                                                 message='Las contraseñas deben coincidir')])
    fecha_nacimiento = DateField('Fecha de Nacimiento', format='%Y-%m-%d', validators=[])
    genero = SelectField('Género', choices=[('M', 'Masculino'), ('F', 'Femenino'), ('O', 'Otro')], validators=[])
    submit = SubmitField('Register')
