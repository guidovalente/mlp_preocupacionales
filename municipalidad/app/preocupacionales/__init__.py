import functools

from flask import (
    Blueprint, render_template, url_for, redirect
)

from flask_wtf import FlaskForm

bp = Blueprint('preocupacionales', __name__, url_prefix='/preocupacionales')

@bp.route('/nuevo_agente', methods=('GET', 'POST'))
def nuevo_agente():
    from .formularios import SimpleForm
    form = SimpleForm()
    if form.validate_on_submit():
        return redirect('/')
    return render_template('preocupacionales/nuevo_agente.html', form=form)
    # return render_template('preocupacionales/nuevo_agente.html')
