from flask_wtf import FlaskForm
from wtforms import (
    StringField, IntegerField, DateTimeField, BooleanField, SelectField
)
from wtforms.validators import InputRequired

class SimpleForm(FlaskForm):
    # name = StringField('name', validators=[DataRequired()])
    fecha = DateTimeField('fecha', format='%d/%m/%Y %H:%M')


class FormularioAgente(FlaskForm):
    """

    Formulario para carga y actualización del agente

    Para pasar las opciones dinámicamente al SelectField, ver la
    documentación de WTForms:
    https://wtforms.readthedocs.io/en/stable/fields.html#basic-fields

    """
    nombre = StringField('Nombre', validators=[InputRequired()])
    apellido = StringField('Apellido', validators=[InputRequired()])
    dni = IntegerField('DNI', validators=[InputRequired()])
    telefono = StringField('Telefono')
    domicilio_calle = StringField('Calle')
    domicilio_numero = StringField('Número')
    domicilio_piso = StringField('Piso')
    domicilio_depto = StringField('Departamento')
    legajo = IntegerField('Legajo')
    reparticion = StringField('Repartición', validators=[InputRequired()])
    turno_psi_1 = DateTimeField('1º Turno', format='%d/%m/%Y %H:%M')
    ausente_psi_1 = BooleanField('Ausente')
    turno_psi_2 = DateTimeField('2º Turno', format='%d/%m/%Y %H:%M')
    ausente_psi_2 = BooleanField('Ausente')
    apto_psi = SelectField(
        'Apto',
        choices=[(None, '-'), (True, 'Sí'), (False, 'No')]
    )
    turno_med_1 = DateTimeField('1º Turno', format='%d/%m/%Y %H:%M')
    ausente_med_1 = BooleanField('Ausente')
    turno_med_2 = DateTimeField('2º Turno', format='%d/%m/%Y %H:%M')
    ausente_med_2 = BooleanField('Ausente')
    apto_med = SelectField(
        'Apto',
        choices=[(None, '-'), (True, 'Sí'), (False, 'No')]
    )
    observaciones = StringField('Observaciones')
