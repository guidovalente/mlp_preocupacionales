from flask_wtf import FlaskForm
from wtforms import (
    StringField, IntegerField, DateTimeField, BooleanField, SelectField,
    TextAreaField, ValidationError
)
from wtforms.validators import InputRequired, Optional

opciones_aptitud = [
    ('None', '-'),
    ('True', 'Sí'),
    ('False', 'No')
]

def opcion_obligatoria(message=None):
    """
    Validador de SelectField

    Esta función valida que haya sido elegido un opción con valor distinto
    a cero (0) en un SelectField.
    En los formularios de esta aplicación, asignamos valor 0 al valor por
    defecto, representado por un guión. De este modo el Select no inicia
    con la primera opción.
    Si la opción seleccionada tiene valor cero, se eleva la ValidationError.

    """
    if not message:
        message = 'Debe elegir una opción válida.'
    def _opcion_obligatoria(form, field):
        if field.data == 0:
            raise ValidationError(message)

    return _opcion_obligatoria


class FormularioAgente(FlaskForm):
    """
    Formulario para carga y actualización del agente

    Para pasar las opciones dinámicamente al SelectField, ver la
    documentación de WTForms:
    https://wtforms.readthedocs.io/en/stable/fields.html#basic-fields

    TODO: agregar campos de calendarios Google Calendar, para asignar un
    calendario a cada turno.

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
    reparticion = SelectField(
        'Repartición',
        coerce=int,
        validators=[
            InputRequired(),
            opcion_obligatoria(message="Debe seleccionar una repartición")
        ]
    )
    turno_psi_1 = DateTimeField('1º Turno', format='%d/%m/%Y %H:%M',
        validators=[Optional()])
    ausente_psi_1 = BooleanField('Ausente')
    turno_psi_2 = DateTimeField('2º Turno', format='%d/%m/%Y %H:%M',
        validators=[Optional()])
    ausente_psi_2 = BooleanField('Ausente')
    apto_psi = SelectField('Apto', choices=opciones_aptitud)
    turno_med_1 = DateTimeField('1º Turno', format='%d/%m/%Y %H:%M',
        validators=[Optional()])
    ausente_med_1 = BooleanField('Ausente')
    turno_med_2 = DateTimeField('2º Turno', format='%d/%m/%Y %H:%M',
        validators=[Optional()])
    ausente_med_2 = BooleanField('Ausente')
    apto_med = SelectField('Apto', choices=opciones_aptitud)
    observaciones = TextAreaField('Observaciones')

    class Meta:
        locales = ['es']

        def get_translations(self, form):
            return super(FlaskForm.Meta, self).get_translations(form)
