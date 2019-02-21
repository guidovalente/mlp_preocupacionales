from flask import Blueprint, redirect, url_for, render_template
from .forms import LoginForm
from app.preocupacionales import bp as bp_preocupacionales

def register_routes(app):
    """Method for registering routes.

    This method will be imported in the factory method to register routes
    with the flask app.
    """
    app.register_blueprint(bp_preocupacionales)

    home_bp = Blueprint('home', __name__, url_prefix='')

    @home_bp.route('/')
    def index():
        return redirect(url_for('preocupacionales.lista'))

    @home_bp.route('/login/', methods=['GET', 'POST'])
    def login():
        form = LoginForm()
        if form.validate_on_submit():
            pass
        return render_template('login.html', title='Ingresar', form=form)

    @home_bp.route('/exito/<int:id>')
    def exito(id): # esta es una vista de prueba, hay que eliminarla
        return render_template('exito.html', id=id)

    app.register_blueprint(home_bp)


    # error page
    @app.errorhandler(404)
    def not_found(error):
        return render_template('404.html'), 404
