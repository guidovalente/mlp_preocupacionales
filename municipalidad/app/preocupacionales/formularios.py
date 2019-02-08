from flask_wtf import FlaskForm
from wtforms import (
    StringField, IntegerField, DateTimeField, BooleanField, SelectField,
    TextAreaField, ValidationError
)
from wtforms.validators import InputRequired, Optional

# Listado de opciones para los campos de apto médico y psicológico
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
    """Formulario para carga y actualización del agente

    TODO: agregar campos de calendarios Google Calendar, para asignar un
    calendario a cada turno.
    """

    def reparticiones_formulario(default="-"):
        """Obtiene la lista de reparticiones de la base de datos.

        Esta función se utiliza para poblar el select de repartición
        del FormularioAgente. Se inserta una opción por defecto que
        se utiliza como placeholder, y luego se insertan la lista de
        reparticiones de la base de datos, correspondientes al modelo
        Repartición de la app.

        El placeholder siempre debe tener el valor cero (0) ya que luego
        será validado por el validador opcion_obligatoria
        """

        from .modelos import Reparticion
        reparticiones = [(0, default)] + Reparticion.query.with_entities(
            Reparticion.id,
            Reparticion.nombre
        ).all()
        return reparticiones

    def asignar_turnos(self, turnos):
        """Función que asigna los valores de los campos de turnos

        Esta función recibe como argumento los turnos de un agente, y con
        esos datos puebla los campos correspondiente del formulario.
        """
        for turno in turnos:
            if turno.tipo == 1:
                if turno.numero == 1:
                    self.turno_psi_1.data = turno.fecha
                elif turno.numero == 2:
                    self.turno_psi_2.data = turno.fecha
            elif turno.tipo == 2:
                if turno.numero == 1:
                    self.turno_med_1.data = turno.fecha
                elif turno.numero == 2:
                    self.turno_med_2.data = turno.fecha

    nombre = StringField('Nombre', validators=[InputRequired()])
    apellido = StringField('Apellido', validators=[InputRequired()])
    dni = IntegerField('DNI', validators=[InputRequired()])
    telefono = StringField('Telefono')
    domicilio_calle = StringField('Calle')
    domicilio_numero = StringField('Número')
    domicilio_piso = StringField('Piso')
    domicilio_depto = StringField('Departamento')
    legajo = IntegerField('Legajo', validators=[Optional()])
    reparticion_id = SelectField(
        'Repartición',
        coerce=int,
        validators=[
            InputRequired(),
            opcion_obligatoria(message="Debe seleccionar una repartición")
        ],
        choices=reparticiones_formulario(default="Elija una repartición...")
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

    # def __init__(self, **kwargs):
    #     agente = kwargs['obj']
    #     from datetime import datetime
    #     print(datetime.now())
    #     agente.turno_med_1=datetime.now()
    #     kwargs['obj'] = agente
    #     super().__init__(**kwargs)

    class Meta:
        locales = ['es']

        def get_translations(self, form):
            return super(FlaskForm.Meta, self).get_translations(form)
