# forms/cliente_form.py
# CSi - CoFre Sistemas Informáticos
# Semana 11: formulario del módulo de Clientes con Flask-WTF y WTForms.
# Reutilizable para registro y edición (ver app.py: vista formulario_cliente).

from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email


class ClienteForm(FlaskForm):
    """Formulario para registrar/editar un cliente de CSi."""

    nombre = StringField(
        'Nombre completo',
        validators=[DataRequired(message='El nombre es obligatorio.'),
                    Length(min=3, max=100, message='Debe tener entre 3 y 100 caracteres.')]
    )

    empresa = StringField(
        'Empresa',
        validators=[DataRequired(message='La empresa es obligatoria.'),
                    Length(min=2, max=120, message='Debe tener entre 2 y 120 caracteres.')]
    )

    correo = StringField(
        'Correo electrónico',
        validators=[DataRequired(message='El correo es obligatorio.'),
                    Email(message='Ingrese un correo electrónico válido.')]
    )

    telefono = StringField(
        'Teléfono',
        validators=[DataRequired(message='El teléfono es obligatorio.'),
                    Length(min=7, max=15, message='Debe tener entre 7 y 15 caracteres.')]
    )

    activo = BooleanField('Cliente activo', default=True)

    submit = SubmitField('Guardar Cliente')
