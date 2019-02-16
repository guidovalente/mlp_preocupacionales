from app.modelo_base import db, Base

class Agente(Base):
    """Modelo de agentes de la municipalidad

    Se relaciona con la reparticion a través del campo reparticion_id, y
    con los turnos a través de los campos de turnos.
    """
    __tablename__ = 'agentes'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(128), nullable=False)
    apellido = db.Column(db.String(128), nullable=False)
    dni = db.Column(db.Integer, nullable=False, unique=True)
    telefono = db.Column(db.String(70), nullable=True)
    domicilio_calle = db.Column(db.String(128), nullable=True)
    domicilio_numero = db.Column(db.String(128), nullable=True)
    domicilio_piso =  db.Column(db.String(128), nullable=True)
    domicilio_depto =  db.Column(db.String(128), nullable=True)
    legajo = db.Column(db.Integer, nullable=True)
    reparticion_id = db.Column(db.Integer,
        db.ForeignKey('reparticiones.id'), nullable=False)
    reparticion = db.relationship('Reparticion')
    apto_psicologico = db.Column(db.Integer, nullable=True)
    apto_medico = db.Column(db.Integer, nullable=True)
    observaciones = db.Column(db.Text, nullable=True)
    turnos = db.relationship('Turno', backref='agente',
        cascade='all, delete-orphan')

    # Los nombres de los turnos no llevan turno_ delante para evitar
    # conflictos de nombre con los campos de turno del formulario
    psi_1 = db.relationship('Turno',
        primaryjoin='and_(Agente.id==Turno.agente_id, '
        'Turno.tipo==1, Turno.numero==1)', uselist=False)
    psi_2 = db.relationship('Turno',
        primaryjoin='and_(Agente.id==Turno.agente_id, '
        'Turno.tipo==1, Turno.numero==2)', uselist=False)
    med_1 = db.relationship('Turno',
        primaryjoin='and_(Agente.id==Turno.agente_id, '
        'Turno.tipo==2, Turno.numero==1)', uselist=False)
    med_2 = db.relationship('Turno',
        primaryjoin='and_(Agente.id==Turno.agente_id, '
        'Turno.tipo==2, Turno.numero==2)', uselist=False)

    def __repr__(self):
        return "Agente {apellido}, {nombre} (DNI: {dni})".format(
            apellido=self.apellido,
            nombre=self.nombre,
            dni=self.dni
        )

    @classmethod
    def con_turnos(cls):
        agente = cls()
        turnos = [
            Turno(tipo=1, numero=1, fecha=None, ausente=False),
            Turno(tipo=1, numero=2, fecha=None, ausente=False),
            Turno(tipo=2, numero=1, fecha=None, ausente=False),
            Turno(tipo=2, numero=2, fecha=None, ausente=False)
        ]
        agente.turnos.extend(turnos)
        return agente


class Reparticion(Base):
    """Modelo de reparticiones de la Municipalidad"""
    __tablename__ = 'reparticiones'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(128), nullable=False, unique=True)

    def __repr__(self):
        return self.nombre


class Turno(Base):
    """Modelo de turnos para preocupacionales

    TODO: agregar campo de Google Calendar para relacionar cada turno
    con su equivalente en Google. De este modo podremos realizar
    modificaciones en los eventos del GCal y almacenar los errores de
    sincronización para reintentar más adelante.
    """
    __tablename__ = 'turnos'

    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.Integer, nullable=False)
    numero = db.Column(db.Integer, nullable=False)
    fecha = db.Column(db.DateTime, nullable=True)
    ausente = db.Column(db.Boolean, nullable=False, default=False)
    agente_id = db.Column(db.Integer, db.ForeignKey('agentes.id'),
        nullable=False)
    calendario_id = db.Column(db.Integer,
        db.ForeignKey('calendarios.id'), nullable=True)
    calendario = db.relationship('Calendario', backref='turnos')


class Calendario(Base):
    __tablename__ = 'calendarios'
    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.Integer, nullable=False)
    nombre = db.Column(db.String(128), nullable=False)
    color = db.Column(db.String(6), nullable=False, default="000000")
