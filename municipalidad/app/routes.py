from flask import Blueprint, redirect, url_for, render_template

def register_routes(app):
    from .helpers import register_commands
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
