from municipalidad import db

# Define a base model for other database tables to inherit
class Base(db.Model):

    __abstract__  = True

    id            = db.Column(db.Integer, primary_key=True)
    date_created  = db.Column(db.DateTime,  default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime,  default=db.func.current_timestamp(),
                                           onupdate=db.func.current_timestamp())

# Define a User model
class Agente(Base):

    id                  = db.Column(db.Integer, primary_key=True)
    nombre              = db.Column(db.String(128), nullable=False)
    apellido            = db.Column(db.String(128), nullable=False)
    dni                 = db.Column(db.Integer, nullable=False, unique=True)
    calle               = db.Column(db.Column(db.String(128), nullable=True))
    numero              = db.Column(db.Column(db.String(128), nullable=True))
    piso                = db.Column(db.Column(db.String(128), nullable=True))
    depto               = db.Column(db.Column(db.String(128), nullable=True))
    legajo              = db.Column(db.Integer, nullable=True)
    reparticion         = db.Column(db.Integer, nullable=False, db.ForeignKey(reparticion.id))
    apto_psicologico    = db.Column(db.Boolean, nullable=True)
    apto_medico         = db.Column(db.Boolean, nullable=True)

    # New instance instantiation procedure
    def __init__(self, name, email, password):

        self.name     = name
        self.email    = email
        self.password = password

    def __repr__(self):
        return '<User %r>' % (self.name)
