# forms/facturacion_form.py
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, FloatField, SubmitField, DateField
from wtforms.validators import DataRequired, NumberRange, Regexp


class FacturacionForm(FlaskForm):
    numero = StringField(
        'N° de factura',
        validators=[
            DataRequired(message='El número de factura es obligatorio.'),
            Regexp(r'^F-\d{3,}$', message='Use el formato F-001, F-002, etc.')
        ]
    )
    cliente = SelectField(
        'Cliente',
        choices=[],
        validators=[DataRequired(message='Seleccione un cliente.')]
    )
    fecha = DateField(
        'Fecha',
        format='%Y-%m-%d',
        validators=[DataRequired(message='La fecha es obligatoria.')]
    )
    total = FloatField(
        'Total (USD)',
        validators=[
            DataRequired(message='El total es obligatorio.'),
            NumberRange(min=0.01, message='El total debe ser mayor a 0.')
        ]
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
