import os
from flask import (
    Flask, render_template, Blueprint, redirect, url_for
)
from .modelo_base import db
from .helpers import register_commands, login_manager, add_time
from .routes import bp as bp_home
from .auth import bp as bp_auth
from .auth.modelos import Usuario
from .preocupacionales import bp as bp_preocupacionales
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

    # initializations
    db.init_app(app) # db
    register_commands(app) # cli commands
    login_manager.init_app(app) # flask-login

    # jinja filters
    app.jinja_env.filters['add_time'] = add_time

    # route blueprints
    app.register_blueprint(bp_home)
    app.register_blueprint(bp_auth)
    app.register_blueprint(bp_preocupacionales)

    @app.errorhandler(404)
    def not_found(error):
        return render_template('404.html'), 404

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
