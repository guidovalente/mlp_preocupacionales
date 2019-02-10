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
        nuevo_agente = Agente.con_turnos()
        form.populate_obj(nuevo_agente)
        db.session.add(nuevo_agente)
        try:
            db.session.commit()
            flash('Agente creado', "border text-center text-success mb-3")
            return redirect(url_for('home.exito', id=nuevo_agente.id))
        except IntegrityError as e:
            db.session.rollback()
            agente_existente = Agente.query.filter_by(dni=nuevo_agente.dni).first()
            if agente_existente is not None:
                error = 'Ya existe un agente con el DNI {} ({} {})'.format(
                    nuevo_agente.dni, agente_existente.nombre,
                    agente_existente.apellido
                )
            else:
                error = e
            flash(error, 'border text-center text-danger mb-3')
    return render_template('preocupacionales/nuevo_agente.html', form=form)

@bp.route('/agente/<int:id>', methods=('GET', 'POST'))
def editar_agente(id):
    from .modelos import Agente
    agente = Agente.query.filter_by(id=id).first()

    if agente is None:
        abort(404)

    from .formularios import FormularioAgente
    form = FormularioAgente(obj=agente)
    if form.validate_on_submit():
        from .modelos import db
        db.session.add(agente)
        form.populate_obj(agente, agente_nuevo=True)
        try:
            db.session.commit()
            flash('Los cambios fueron guardados',
                'border text-center text-success mb-3')
        except IntegrityError as e:
            db.session.rollback()
            agente_existente = Agente.query.filter_by(dni=form.dni.data).first()
            if agente_existente is not None:
                error = 'Ya existe un agente con el DNI {} ({} {})'.format(
                    form.dni.data, agente_existente.nombre,
                    agente_existente.apellido
                )
                form.dni.errors.append("DNI original: {}".format(agente.dni))
            else:
                error = e
            flash(error, 'border text-center text-danger mb-3')
    elif form.errors:
        flash(form.errors)
    return render_template('preocupacionales/editar_agente.html', form=form, id=id)
