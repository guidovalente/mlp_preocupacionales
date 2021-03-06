import click
from flask.cli import with_appcontext
from flask_login import LoginManager
from flask_migrate import Migrate
from app.preocupacionales.modelos import (
    Agente, Turno, Reparticion, Calendario
)
import random
from .modelo_base import db
from .auth.modelos import Usuario, Rol, Permiso
from .preocupacionales.modelos import Agente, Reparticion
from datetime import timedelta


migrate = Migrate()


def get_shell(app):
    @app.shell_context_processor
    def make_shell_context():
        return {
            'db': db,
            'Usuario': Usuario,
            'Rol': Rol,
            'Permiso': Permiso,
            'Agente': Agente,
            'Reparticion': Reparticion,
            'Turno': Turno,
            'Calendario': Calendario
        }
    return make_shell_context

def add_time(value, minutes=0, days=0):
    return value + timedelta(minutes=minutes, days=days)


# iniciamos y configuramos flask-login
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Debe ingresar para ver esta página.'

@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))


@click.command('init-db')
@with_appcontext
def init_db_command():
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
        etiqueta='UPA Los Hornos'),
        Calendario(tipo=2, nombre=('el laboratorio central del área "A", '
            'consultorios externos, del Hospital San Juan de Dios'),
        direccion='calle 27 y 70, Planta Baja',
        etiqueta='Hospital San Juan de Dios')
    ]
    db.session.add(reparticion)
    db.session.commit()
    db.session.bulk_save_objects(calendarios)
    db.session.commit()
    Rol.insertar_roles()


@click.command('insert-test-records')
@with_appcontext
def insert_test_records():
    nombres = ['Pedro', 'María', 'Juan', 'Pablo', 'Julieta', 'Guido']
    apellidos = ['Pérez', 'Giménez', 'Rodríguez', 'Blanco', 'Negro']
    reparticiones = Reparticion.query.count()
    print("Comenzando inserción de registros de prueba")
    for i in range(300):
        print("Insertando registro {}".format(str(i+1)), end='\r', flush=True)
        agente = Agente.con_turnos(
            nombre=random.choice(nombres),
            apellido=random.choice(apellidos),
            dni=random.randint(1,99999999),
            telefono=random.randint(1,7777777),
            legajo=random.randint(717000,717999),
            reparticion_id=random.randint(1, reparticiones),
            observaciones="Agente de prueba."
        )
        db.session.add(agente)
        db.session.commit()


def register_commands(app):
    app.cli.add_command(init_db_command)
    app.cli.add_command(insert_test_records)
