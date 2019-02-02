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
    # de repartición. Al principio le insertamos una opción vacía
    # para que no comience con ninguna repartición elegida.
    form = FormularioAgente()
    reparticiones = [(0, '-')] + Reparticion.query.with_entities(
        Reparticion.id,
        Reparticion.nombre
    ).all()
    if len(reparticiones) < 1:
        flash('No existen reparticiones cargadas, por lo que no podrá guardar nuevos agentes.')
    form.reparticion.choices = reparticiones
    if form.validate_on_submit():
        nuevo_agente = Agente()
        form.populate_obj(nuevo_agente)

        db.session.add(nuevo_agente)
        db.session.commit()
        return redirect('/')
    return render_template('preocupacionales/nuevo_agente.html', form=form)
