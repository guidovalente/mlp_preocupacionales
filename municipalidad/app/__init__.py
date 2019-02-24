import os
from flask import (
    Flask, render_template, Blueprint, redirect, url_for
)
from .modelo_base import db
from .routes import register_routes
from .helpers import register_commands
from .modelos import Usuario
from .preocupacionales.modelos import (
    Agente, Reparticion, Turno, Calendario
)


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py')
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # get the database
    db.init_app(app)
    register_routes(app)
    register_commands(app)
    app.jinja_env.filters['add_time'] = add_time

    # shell context
    @app.shell_context_processor
    def make_shell_context():
        return {
            'db': db,
            'Usuario': Usuario,
            'Agente': Agente,
            'Reparticion': Reparticion,
            'Turno': Turno,
            'Calendario': Calendario
        }

    return app
