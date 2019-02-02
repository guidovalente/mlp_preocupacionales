import functools

from flask import (
    Blueprint, render_template, url_for, redirect, flash, current_app
)

bp = Blueprint('preocupacionales', __name__, url_prefix='/preocupacionales')

@bp.route('/nuevo_agente', methods=('GET', 'POST'))
def nuevo_agente():
    from .formularios import FormularioAgente
    from .modelos import Reparticion

    # Inicializamos el formulario y luego le asignamos las opciones
    # de repartición.
    form = FormularioAgente()
    # form.reparticion.choices = FormularioAgente.reparticiones_formulario(default="Elija una repartición...")
    if form.validate_on_submit():
        from .modelos import Agente, db
        nuevo_agente = Agente()
        form.populate_obj(nuevo_agente)
        nuevo_agente.reparticion = db.session.query(Reparticion).filter_by(id=form.reparticion.data).first()

        db.session.add(nuevo_agente)
        db.session.commit()
        return redirect('/')
    return render_template('preocupacionales/nuevo_agente.html', form=form)
