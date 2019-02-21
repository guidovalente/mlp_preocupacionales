import click
from flask.cli import with_appcontext


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

@click.command('insert-test-records')
@with_appcontext
def insert_test_records():
    nombres = ['Pedro', 'María', 'Martina', 'Lucas', 'Victoria', 'Guido',
        'Matías', 'Lucrecia']
    apellidos = ['Quattrini', 'Varlotta', 'Morón', 'Valente', 'Smeriglio',
        'Zappa']
    import random
    from .preocupacionales.modelos import Agente, Reparticion
    reparticiones = Reparticion.query.count()
    print("Comenzando inserción de registros de prueba")
    import sys
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
