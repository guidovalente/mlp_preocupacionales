from .modelos_base import db, Base

class Agente(Base):
    __tablename__ = 'agentes'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(128), nullable=False)
    apellido = db.Column(db.String(128), nullable=False)
    dni = db.Column(db.Integer, nullable=False, unique=True)
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
    turnos = db.relationship('Turno', cascade="all,delete",
        backref='agente', lazy=True)

    def __init__(
            self, nombre, apellido, reparticion, dni, domicilio_calle=None,
            domicilio_numero=None, domicilio_piso=None,
            domicilio_depto=None, legajo=None,
            apto_psicologico=None, apto_medico=None,
            turnos=None):

        self.nombre = nombre
        self.apellido = apellido
        self.dni = dni
        self.domicilio_calle = domicilio_calle
        self.domicilio_numero = domicilio_numero
        self.domicilio_piso = domicilio_piso
        self.domicilio_depto = domicilio_depto
        self.legajo = legajo
        self.reparticion = reparticion
        self.apto_psicologico = apto_psicologico
        self.apto_medico = apto_medico
        self.turnos = turnos

    def __repr__(self):
        return "Agente {apellido}, {nombre} (DNI: {dni})".format(self.apellido, self.nombre, self.dni)


class Reparticion(Base):
    __tablename__ = 'reparticiones'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(128), nullable=False)

    def __init__(self, nombre):
        self.nombre = nombre

    def __repr__(self):
        return "Reparticion {}".format(self.nombre)


class Turno(Base):
    __tablename__ = 'turnos'

    id = db.Column(db.Integer, primary_key=True)
    numero = db.Column(db.Integer, nullable=False)
    tipo = db.Column(db.Integer, nullable=False)
    fecha = db.Column(db.DateTime, nullable=True, unique=True)
    ausente = db.Column(db.Boolean, nullable=False, default=False)
    id_agente = db.Column(db.Integer, db.ForeignKey('agentes.id'),
                            nullable=False)

    # def __init__(
    #         self, numero)

class Simple(Base):
    __tablename__ = "simples"
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.Integer, nullable=False)

    def __init__(self, nombre):
        self.nombre = nombre

    def __repr__(self):
        return "Simple: {}".format(self.nombre)
