import functools

from flask import (
    Blueprint, render_template, url_for
)

from flask_wtf import FlaskForm
from .modelos import Agente

bp = Blueprint('preocupacionales', __name__, url_prefix='/preocupacionales')

@bp.route('/nuevo_agente', methods=('GET', 'POST'))
def nuevo_agente():

    return render_template('preocupacionales/nuevo_agente.html')
