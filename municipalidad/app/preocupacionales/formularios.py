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
    nombre = StringField('nombre', validator=[InputRequired()])
    apellido = StringField('apellido', validator=[InputRequired()])
    dni = IntegerField('dni', validator=[InputRequired()])
    domicilio_calle = StringField('domicilio_calle')
    domicilio_numero = StringField('domicilio_numero')
    domicilio_piso = StringField('domicilio_piso')
    domicilio_depto = StringField('domicilio_depto')
    legajo = IntegerField('dni')
    reparticion = StringField('nombre', validator=[InputRequired()])
    turno_psi_1 = DateTimeField('turno_psi_1', format='%d/%m/%Y %H:%M')
    ausente_psi_1 = BooleanField('ausente_psi_1')
    turno_psi_2 = DateTimeField('turno_psi_2', format='%d/%m/%Y %H:%M')
    ausente_psi_2 = BooleanField('ausente_psi_2')
    apto_psi = SelectField('apto_psi', choices=['-', 'Sí', 'No'])
    turno_med_1 = DateTimeField('turno_med_1', format='%d/%m/%Y %H:%M')
    ausente_med_1 = BooleanField('ausente_med_1')
    turno_med_2 = DateTimeField('turno_med_2', format='%d/%m/%Y %H:%M')
    ausente_med_2 = BooleanField('ausente_med_2')
    apto_med = SelectField('apto_med', choices=['-', 'Sí', 'No'])
    observaciones = StringField('observaciones')
