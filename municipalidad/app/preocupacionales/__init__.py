import functools

from flask import (
    Blueprint, render_template, url_for, redirect, flash, current_app
)

bp = Blueprint('preocupacionales', __name__, url_prefix='/preocupacionales')

@bp.route('/nuevo_agente', methods=('GET', 'POST'))
def nuevo_agente():
    # Prueba de modelos
    # from .modelos import Agente, Reparticion
    # guido = Agente(
    #     nombre="Guido",
    #     apellido="Valente",
    #     dni=37151819,
    #     reparticion=Reparticion(nombre="dgp")
    # )

    from .formularios import FormularioAgente
    form = FormularioAgente()
    print(form.meta.get_translations(form))
    if form.validate_on_submit():
        # print(form.nombre.text)
        from .modelos import Agente, Reparticion, db
        # nuevo_agente = Agente(
        #     nombre="Guido",
        #     apellido="Valente",
        #     dni=234234234,
        #     reparticion=reparticion
        # )
        # nuevo_agente = Agente(
        #     nombre=form.nombre.data,
        #     apellido=form.apellido.data,
        #     dni=form.dni.data,
        #     reparticion=db.session.query(Reparticion).filter_by(nombre=form.reparticion.data).first()
        # )
        nuevo_agente = Agente()
        form.populate_obj(nuevo_agente)
        nuevo_agente.reparticion = db.session.query(Reparticion).filter_by(nombre=form.reparticion.data).first()

        db.session.add(nuevo_agente)
        db.session.commit()
        return redirect('/')
    elif form.errors:
        print('turno_psi_1' in form.errors)
        for field, errors in form.errors.items():
            for error in errors:
                print(field, error)
    return render_template('preocupacionales/nuevo_agente.html', form=form)
