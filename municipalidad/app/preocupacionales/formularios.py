from flask_wtf import FlaskForm
from wtforms import (
    StringField, IntegerField, DateTimeField, BooleanField, SelectField,
    TextAreaField, ValidationError
)
from wtforms.validators import InputRequired, Optional
import datetime
from .modelos import Reparticion, Calendario

def opcion_valida(message=None):
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
    def _opcion_valida(form, field):
        if field.data == 0:
            raise ValidationError(message)

    return _opcion_valida


class Weekday(object):
    def __init__(self, message=None):
        self.message = message

    def __call__(self, form, field):
        if field.data.weekday() > 4:
            print(field.data.weekday())
            if self.message is None:
                message = "Debe seleccionar un día de la semana"
            else:
                message = self.message
            field.errors[:] = []
            raise ValidationError(message)



class FormularioAgente(FlaskForm):
    """Formulario base para carga y actualización del agente

    Luego será extendido por las subclases respectivas (de creación
    y de edición de agente).
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.reparticion_id.choices = self.opciones_reparticiones(
        default="Elija una repartición...")

    class Meta:
            locales = ['es']

            def get_translations(self, form):
                return super(FlaskForm.Meta, self).get_translations(form)

    def opciones_reparticiones(self, default="-"):
        """Obtiene la lista de reparticiones de la base de datos.

        Esta función se utiliza para poblar el select de repartición
        del FormularioAgente. Se inserta una opción por defecto que
        se utiliza como placeholder, y luego se insertan la lista de
        reparticiones de la base de datos, correspondientes al modelo
        Repartición de la app.

        El placeholder siempre debe tener el valor cero (0) ya que luego
        será validado por el validador opcion_valida
        """
        reparticiones = [(0, default)] + Reparticion.query.with_entities(
            Reparticion.id,
            Reparticion.nombre
        ).all()
        return reparticiones

    # campos del formulario
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
            opcion_valida(message="Debe seleccionar una repartición")
        ]
    )
    observaciones = TextAreaField('Observaciones')


class FormularioEditarAgente(FormularioAgente):
    """Clase de FormularioAgente extendida para edición

    Este clase hereda el formulario de nuevo_agente y le agrega campos
    y métodos para la edición de un agente, principalmente lo relacionado
    a los turnos.
    """
    def __init__(self, **kwargs):
        """Sobreescritura del método init para asignar turnos

        Solamente nos interesa modificar este método si el llamado al
        formulario se hizo desde la vista de editar_agente. En este caso
        habrá un argumento en kwargs llamado 'obj'. De no haberlo, no
        modificaremos el comportamiento del método y simplemente dejaremos
        que siga su curso.
        """
        self.poblar_turnos(kwargs['obj'])
        super().__init__(**kwargs)
        self.cal_psi_1.choices = self.opciones_calendarios(1)
        self.cal_psi_2.choices = self.opciones_calendarios(1)
        self.cal_med_1.choices = self.opciones_calendarios(2)
        self.cal_med_2.choices = self.opciones_calendarios(2)

    def populate_obj(self, obj, edicion=False):
        """Sobreescritura del método para guardado de turnos

        Cuando se puebla el objeto en base a los datos del formulario,
        realizamos el guardado de los turnos, ya que pertenecen a una
        clase diferente.
        """
        super().populate_obj(obj)
        self.guardar_turnos(obj)

    def validate(self):
        """Sobreescritura de validate para validar turnos y calendarios

        Este método verifica que haya un calendario seleccionado si los
        campos de turnos son completados por el usuario.
        De este modo no queda ningún turno cargado sin calendario asignado.

        NOTE: la llamada al método de validación original hay que hacerla al
        principio para que se generen las listas de errores a los que luego
        vamos a anexar los errores que ocurran en la validación realizada
        en la sobreescritura. De lo contrario el método append dará error.
        """
        if not super().validate():
            return False
        turnos = [ self.turno_psi_1, self.turno_psi_2,
            self.turno_med_1, self.turno_med_2]
        calendarios = [self.cal_psi_1, self.cal_psi_2,
            self.cal_med_1, self.cal_med_2]
        assert len(turnos) == len(calendarios),('La cantidad de campos de '
            'turnos y calendarios debe ser igual.')
        error_status = False
        for i in range(len(turnos)):
            if turnos[i].data and calendarios[i].data == 0:
                error_status = True
                calendarios[i].errors.append('Debe asignar un calendario.')
        if error_status:
            return False
        return True

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
            setattr(agente,
                'cal_{}_{}'.format(tipo(turno.tipo), turno.numero),
                turno.calendario_id)

    def guardar_turnos(self, agente):
        """Guarda los turnos en la instancia de Agente

        Esta función toma los campos de turnos y los anexa al objeto Agente
        para que sean guardados como sus respectivos turnos en la base de
        datos.
        """
        agente.psi_1.fecha = self.turno_psi_1.data
        agente.psi_1.ausente = self.ausente_psi_1.data
        agente.psi_1.calendario_id = self.cal_psi_1.data
        agente.psi_2.fecha = self.turno_psi_2.data
        agente.psi_2.ausente = self.ausente_psi_2.data
        agente.psi_2.calendario_id = self.cal_psi_2.data
        agente.med_1.fecha = self.turno_med_1.data
        agente.med_1.ausente = self.ausente_med_1.data
        agente.med_1.calendario_id = self.cal_med_1.data
        agente.med_2.fecha = self.turno_med_2.data
        agente.med_2.ausente = self.ausente_med_2.data
        agente.med_2.calendario_id = self.cal_med_2.data

    def opciones_calendarios(self, tipo):
        """Método para obtener los calendarios y mostrarlos en un SelectField
        """
        calendarios = {
            1: Calendario.query.with_entities(Calendario.id,
                Calendario.etiqueta).filter_by(tipo=1).all(),
            2:Calendario.query.with_entities(Calendario.id,
                Calendario.etiqueta).filter_by(tipo=2).all(),
        }
        return [(0, '-')] + calendarios[tipo]

    # Listado de opciones para los campos de apto médico y psicológico
    opciones_aptitud = [
        (0, 'Pendiente'),
        (1, 'Sí'),
        (2, 'No')
    ]

    turno_psi_1 = DateTimeField('1º Turno', format='%d/%m/%Y %H:%M',
        validators=[Optional(), Weekday()])
    cal_psi_1 = SelectField(validators=[Optional()], coerce=int)
    ausente_psi_1 = BooleanField('Ausente')
    turno_psi_2 = DateTimeField('2º Turno', format='%d/%m/%Y %H:%M',
        validators=[Optional(), Weekday()])
    cal_psi_2 = SelectField(validators=[Optional()], coerce=int)
    ausente_psi_2 = BooleanField('Ausente')
    apto_psi = SelectField('Apto', choices=opciones_aptitud,
        coerce=int)
    turno_med_1 = DateTimeField('1º Turno', format='%d/%m/%Y %H:%M',
        validators=[Optional(), Weekday()])
    cal_med_1 = SelectField(validators=[Optional()], coerce=int)
    ausente_med_1 = BooleanField('Ausente')
    turno_med_2 = DateTimeField('2º Turno', format='%d/%m/%Y %H:%M',
        validators=[Optional(), Weekday()])
    cal_med_2 = SelectField(validators=[Optional()], coerce=int)
    ausente_med_2 = BooleanField('Ausente')
    apto_med = SelectField('Apto', choices=opciones_aptitud,
        coerce=int)
