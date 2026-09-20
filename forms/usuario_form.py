# forms/usuario_form.py
# CSi - CoFre Sistemas Informáticos
# Semana 14: formulario de registro de usuarios del sistema (para poder
# iniciar sesión). La contraseña NUNCA se guarda tal como llega aquí:
# app.py la transforma con generate_password_hash() antes del INSERT
# (ver la ruta /registro).

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo


class UsuarioForm(FlaskForm):
    """Formulario para registrar un nuevo usuario autorizado a ingresar
    al sistema (tabla 'usuarios')."""

    usuario = StringField(
        'Usuario',
        validators=[DataRequired(message='El usuario es obligatorio.'),
                    Length(min=4, max=50, message='Debe tener entre 4 y 50 caracteres.')]
    )

    password = PasswordField(
        'Contraseña',
        validators=[DataRequired(message='La contraseña es obligatoria.'),
                    Length(min=6, message='Debe tener al menos 6 caracteres.')]
    )

    confirmar_password = PasswordField(
        'Confirmar contraseña',
        validators=[DataRequired(message='Debes confirmar la contraseña.'),
                    EqualTo('password', message='Las contraseñas no coinciden.')]
    )

    submit = SubmitField('Registrarse')
