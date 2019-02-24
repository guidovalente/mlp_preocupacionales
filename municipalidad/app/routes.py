from flask import Blueprint, redirect, url_for, render_template
from flask_login import login_required

bp = Blueprint('home', __name__, url_prefix='')

@bp.route('/')
@login_required
def index():
    return redirect(url_for('preocupacionales.lista'))

@bp.route('/exito/<int:id>')
def exito(id): # esta es una vista de prueba, hay que eliminarla
    return render_template('exito.html', id=id)
