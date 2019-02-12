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

    def poblar_turnos(self, agente):
        """Función que asigna los valores de los campos de turnos

        Esta función recibe como argumento la instancia del agente y crea
        un atributo para cada turno del formulario. Al ser llamada desde el
        constructor __init__ antes de que se cree la instancia, al momento
        de llenar el formulario con los datos del objeto el mismo ya tendrá
        como atributos los datos sobre los turnos (fecha y ausente).
        """
        turnos = agente.turnos
        tipo = lambda x: 'psi' if x == 1 else 'med'
        for turno in turnos:
            setattr(agente,
                'turno_{}_{}'.format(tipo(turno.tipo), turno.numero),
                turno.fecha)
            setattr(agente,
                'ausente_{}_{}'.format(tipo(turno.tipo), turno.numero),
                turno.ausente)

    def guardar_turnos(self, agente):
        """Guarda los turnos en la instancia de Agente

        Esta función toma los campos de turnos y los anexa al objeto Agente
        para que sean guardados como sus respectivos turnos en la base de
        datos.
        """
        agente.psi_1.fecha = self.turno_psi_1.data
        agente.psi_1.ausente = self.ausente_psi_1.data
        agente.psi_2.fecha = self.turno_psi_2.data
        agente.psi_2.ausente = self.ausente_psi_2.data
        agente.med_1.fecha = self.turno_med_1.data
        agente.med_1.ausente = self.ausente_med_1.data
        agente.med_2.fecha = self.turno_med_2.data
        agente.med_2.ausente = self.ausente_med_2.data

    def __init__(self, **kwargs):
        """Sobreescritura del método init para asignar turnos

        Solamente nos interesa modificar este método si el llamado al
        formulario se hizo desde la vista de editar_agente. En este caso
        habrá un argumento en kwargs llamado 'obj'. De no haberlo, no
        modificaremos el comportamiento del método y simplemente dejaremos
        que siga su curso.
        """
        if 'obj' in kwargs:
            self.poblar_turnos(kwargs['obj'])
        super().__init__(**kwargs)

    def populate_obj(self, obj, edicion=False):
        super().populate_obj(obj)
        if edicion:
            self.guardar_turnos(obj)

    class Meta:
            locales = ['es']

            def get_translations(self, form):
                return super(FlaskForm.Meta, self).get_translations(form)

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
