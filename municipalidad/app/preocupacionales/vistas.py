from app.modelo_base import db
from sqlalchemy.orm import mapper

class AgentesPendientes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tipo_turno = db.Column(db.Integer)
    nombre = db.Column(db.String)
    apellido = db.Column(db.String)
    dni = db.Column(db.Integer)
    legajo = db.Column(db.Integer)
    reparticion_id = db.Column(db.Integer, db.ForeignKey('reparticiones.id'))
    reparticion = db.relationship('Reparticion')
    apto_psi = db.Column(db.Integer)
    apto_med = db.Column(db.Integer)
