import os
from flask import Flask, render_template, Blueprint, redirect, url_for
from .modelo_base import db
from .helpers import (
    register_commands, login_manager, add_time, get_shell, migrate
)
from .routes import bp as bp_home
from .auth import bp as bp_auth
from .preocupacionales import bp as bp_preocupacionales


def create_app(instance_path):
    # create and configure the app
    app = Flask(__name__,
        instance_path=instance_path,
        instance_relative_config=True)

    app.config.from_pyfile('config.py')

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # initializations
    db.init_app(app) # db
    register_commands(app) # cli commands
    get_shell(app) # flask shell
    login_manager.init_app(app) # flask-login
    migrate.init_app(app, db)

    # jinja filters
    app.jinja_env.filters['add_time'] = add_time

    # route blueprints
    app.register_blueprint(bp_home)
    app.register_blueprint(bp_auth)
    app.register_blueprint(bp_preocupacionales)

    @app.errorhandler(404)
    def not_found(error):
        return render_template('error.html',
            mensaje=("La página buscada no existe. Si cree que esto es un "
            "error contáctese con el administrador del sistema.")), 404

    @app.errorhandler(403)
    def forbidden(error):
        return render_template('error.html',
            mensaje='No tiene permiso para ver esta página.'), 403

    return app
