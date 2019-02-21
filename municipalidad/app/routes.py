from flask import Blueprint, redirect, url_for, render_template

def register_routes(app):
    """Method for registering routes.

    This method will be imported in the factory method to register routes
    with the flask app.
    """
    home_bp = Blueprint('home', __name__, url_prefix='')
    @home_bp.route('/exito/<int:id>')
    def exito(id): # esta es una vista de prueba, hay que eliminarla
        return render_template('exito.html', id=id)

    @home_bp.route('/')
    def index():
        return redirect(url_for('preocupacionales.lista'))

    app.register_blueprint(home_bp)

    from . import preocupacionales
    app.register_blueprint(preocupacionales.bp)

    # error page
    @app.errorhandler(404)
    def not_found(error):
        return render_template('404.html'), 404
