from flask import (
    Blueprint, render_template, url_for, redirect, flash, current_app, abort
)
from sqlalchemy.exc import IntegrityError

bp = Blueprint('preocupacionales', __name__, url_prefix='/preocupacionales')

@bp.route('/nuevo_agente', methods=('GET', 'POST'))
def nuevo_agente():
    from .formularios import FormularioAgente
    from .modelos import Reparticion
    form = FormularioAgente()

    if form.validate_on_submit():
        from .modelos import Agente, db
        nuevo_agente = Agente()
        form.populate_obj(nuevo_agente)
        db.session.add(nuevo_agente)
        try:
            db.session.commit()
            flash('Agente creado', "border text-center text-success mb-3")
            return redirect('/exito')
        except IntegrityError: # si el dni ya existe en la tabla de agentes
            db.session.rollback()
            flash("Ya existe un agente con ese DNI", "border text-center text-danger mb-3")
    return render_template('preocupacionales/nuevo_agente.html', form=form)

@bp.route('/agente/<int:id>')
def editar_agente(id):
    from .modelos import Agente
    agente = Agente.query.filter_by(id=id).first()
    # print(agente.turno_psi_1)

    if agente is None:
        abort(404)

    from .formularios import FormularioAgente
    form = FormularioAgente(obj=agente)
    return render_template('preocupacionales/nuevo_agente.html', form=form)
