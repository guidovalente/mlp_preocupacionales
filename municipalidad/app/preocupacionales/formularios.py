from flask_wtf import FlaskForm
from wtforms import (
    StringField, IntegerField, DateTimeField, BooleanField, SelectField,
    TextAreaField
)
from wtforms.validators import InputRequired, Optional

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
    legajo = IntegerField('Legajo', validators=[Optional()])
    reparticion = StringField('Repartición', validators=[InputRequired()])
    turno_psi_1 = DateTimeField('1º Turno', format='%d/%m/%Y %H:%M',
        validators=[Optional()])
    ausente_psi_1 = BooleanField('Ausente')
    turno_psi_2 = DateTimeField('2º Turno', format='%d/%m/%Y %H:%M',
        validators=[Optional()])
    ausente_psi_2 = BooleanField('Ausente')
    apto_psi = SelectField(
        'Apto',
        choices=[('None', '-'), ('True', 'Sí'), ('False', 'No')]
    )
    turno_med_1 = DateTimeField('1º Turno', format='%d/%m/%Y %H:%M',
        validators=[Optional()])
    ausente_med_1 = BooleanField('Ausente')
    turno_med_2 = DateTimeField('2º Turno', format='%d/%m/%Y %H:%M',
        validators=[Optional()])
    ausente_med_2 = BooleanField('Ausente')
    apto_med = SelectField(
        'Apto',
        choices=[('None', '-'), ('True', 'Sí'), ('False', 'No')]
    )
    observaciones = TextAreaField('Observaciones')

    class Meta:
        locales = ['es']

        def get_translations(self, form):
            return super(FlaskForm.Meta, self).get_translations(form)
