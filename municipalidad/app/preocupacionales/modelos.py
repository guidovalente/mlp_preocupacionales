from app.modelo_base import db, Base

class Agente(Base):
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
    apto_psicologico = db.Column(db.Boolean, nullable=True)
    apto_medico = db.Column(db.Boolean, nullable=True)
    observaciones = db.Column(db.Text, nullable=True)

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


class Reparticion(Base):
    __tablename__ = 'reparticiones'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(128), nullable=False, unique=True)

    def __repr__(self):
        return self.nombre

class Turno(Base):
    """
    Modelo de turnos para preocupacionales

    TODO: agregar campo de Google Calendar para relacionar cada turno
    con su equivalente en Google. De este modo podremos realizar
    modificaciones en los eventos del GCal y almacenar los errores de
    sincronización para reintentar más adelante.
    """
    __tablename__ = 'turnos'

    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.Integer, nullable=False)
    numero = db.Column(db.Integer, nullable=False)
    fecha = db.Column(db.DateTime, nullable=True, unique=True)
    ausente = db.Column(db.Boolean, nullable=False, default=False)
    agente_id = db.Column(db.Integer, db.ForeignKey('agentes.id'),
                            nullable=False)
    agente = db.relationship('Agente', backref='turnos', lazy=True, uselist=False)
