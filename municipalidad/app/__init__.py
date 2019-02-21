import os

from flask import (
    Flask, render_template, Blueprint, redirect, url_for
)


def add_time(value, minutes=0, days=0):
    from datetime import timedelta
    return value + timedelta(minutes=minutes, days=days)

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

    from .modelo_base import db, register_commands
    db.init_app(app)
    register_commands(app)

    from . import preocupacionales
    app.register_blueprint(preocupacionales.bp)

    home_bp = Blueprint('home', __name__, url_prefix='')
    @home_bp.route('/exito/<int:id>')
    def exito(id):
        return render_template('exito.html', id=id)

    @home_bp.route('/')
    def index():
        return redirect(url_for('preocupacionales.lista'))

    app.register_blueprint(home_bp)

    @app.errorhandler(404)
    def not_found(error):
        return render_template('404.html'), 404

    from datetime import timedelta
    app.jinja_env.filters['add_time'] = add_time

    return app
