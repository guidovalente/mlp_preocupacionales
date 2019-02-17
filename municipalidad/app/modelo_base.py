from flask_sqlalchemy import SQLAlchemy
import click
from flask.cli import with_appcontext

db = SQLAlchemy()

# Define a base model for other database tables to inherit
class Base(db.Model):

    __abstract__  = True

    id            = db.Column(db.Integer, primary_key=True)
    date_created  = db.Column(db.DateTime,  default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime,  default=db.func.current_timestamp(),
                                           onupdate=db.func.current_timestamp())

@click.command('init-db')
@with_appcontext
def init_db_command():
    from app.preocupacionales.modelos import (
        Agente, Turno, Reparticion, Calendario
    )
    db.create_all()
    reparticion = Reparticion(nombre='DGP')
    calendarios = [
        Calendario(tipo=1, nombre='el Departamento de Carpetas Médicas',
        direccion='calle 12 entre 50 y 51, Torre I, Piso 3',
        etiqueta='Mañana'),
        Calendario(tipo=1, nombre='el Departamento de Carpetas Médicas',
        direccion='calle 12 entre 50 y 51, Torre I, Piso 3',
        etiqueta='Tarde'),
        Calendario(tipo=2, nombre='la UPA de Los Hornos',
        direccion='calle 44 y ciento algo',
        etiqueta='UPA'),
        Calendario(tipo=2, nombre=('el laboratorio central del área "A", '
            'consultorios externos, del Hospital San Juan de Dios'),
        direccion='calle 27 y 70, Planta Baja',
        etiqueta='San Juan')
    ]
    db.session.add(reparticion)
    db.session.commit()
    db.session.bulk_save_objects(calendarios)
    db.session.commit()


def register_commands(app):
    app.cli.add_command(init_db_command)
