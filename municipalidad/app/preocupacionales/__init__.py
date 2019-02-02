import functools

from flask import (
    Blueprint, render_template, url_for, redirect, flash, current_app
)

bp = Blueprint('preocupacionales', __name__, url_prefix='/preocupacionales')

@bp.route('/nuevo_agente', methods=('GET', 'POST'))
def nuevo_agente():
    from .formularios import FormularioAgente
    form = FormularioAgente()
    if form.validate_on_submit():
        nuevo_agente = Agente()
        form.populate_obj(nuevo_agente)

        db.session.add(nuevo_agente)
        db.session.commit()
        return redirect('/')
    return render_template('preocupacionales/nuevo_agente.html', form=form)
