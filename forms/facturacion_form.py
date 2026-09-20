# forms/facturacion_form.py
# CSi - CoFre Sistemas Informáticos
# Semana 11: formulario del módulo de Facturación con Flask-WTF y WTForms.
# Reutilizable para registro y edición (ver app.py: vista formulario_facturacion).

from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, FloatField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange, Regexp


class FacturacionForm(FlaskForm):
    """Formulario para registrar/editar una factura de CSi."""

    numero = StringField(
        'N° de factura',
        validators=[DataRequired(message='El número de factura es obligatorio.'),
                    Regexp(r'^F-\d{3,}$', message='Use el formato F-001, F-002, etc.')]
    )

    cliente = StringField(
        'Cliente',
        validators=[DataRequired(message='El cliente es obligatorio.'),
                    Length(min=3, max=100, message='Debe tener entre 3 y 100 caracteres.')]
    )

    fecha = StringField(
        'Fecha (AAAA-MM-DD)',
        validators=[DataRequired(message='La fecha es obligatoria.'),
                    Regexp(r'^\d{4}-\d{2}-\d{2}$', message='Use el formato AAAA-MM-DD.')]
    )

    total = FloatField(
        'Total (USD)',
        validators=[DataRequired(message='El total es obligatorio.'),
                    NumberRange(min=0.01, message='El total debe ser mayor a 0.')]
    )

    estado = SelectField(
        'Estado',
        choices=[
            ('Pagada', 'Pagada'),
            ('Pendiente', 'Pendiente'),
            ('Anulada', 'Anulada'),
        ],
        validators=[DataRequired(message='Seleccione un estado.')]
    )

    submit = SubmitField('Guardar Factura')
