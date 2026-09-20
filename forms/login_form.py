# forms/login_form.py
# CSi - CoFre Sistemas Informáticos
# Semana 14: formulario de inicio de sesión. Solo valida que ambos campos
# estén presentes; la comprobación real de las credenciales (existencia
# del usuario + check_password_hash) ocurre en la ruta /login de app.py,
# nunca comparando la contraseña escrita directamente contra la
# almacenada en la base de datos.

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    """Formulario de inicio de sesión (usuario + contraseña)."""

    usuario = StringField(
        'Usuario',
        validators=[DataRequired(message='El usuario es obligatorio.')]
    )

    password = PasswordField(
        'Contraseña',
        validators=[DataRequired(message='La contraseña es obligatoria.')]
    )

    submit = SubmitField('Iniciar sesión')
