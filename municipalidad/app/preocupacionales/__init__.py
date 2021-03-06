from flask import (
    Blueprint, render_template, url_for, redirect, flash, current_app, abort,
    request
)
from flask_login import login_required
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError
from datetime import datetime
from .modelos import db, Agente, Reparticion, Turno, Calendario
from .formularios import FormularioAgente, FormularioEditarAgente
from app.auth.modelos import Permiso
from app.auth.decorators import permission_required

bp = Blueprint('preocupacionales', __name__, url_prefix='/preocupacionales')


@bp.route('/')
@login_required
def index():
    return redirect(url_for('preocupacionales.lista'))


@bp.route('/nuevo_agente/', methods=('GET', 'POST'))
@login_required
@permission_required(Permiso.CREAR_AGENTE)
def nuevo_agente():
    form = FormularioAgente()
    if form.validate_on_submit():
        nuevo_agente = Agente.con_turnos()
        form.populate_obj(nuevo_agente)
        db.session.add(nuevo_agente)
        try:
            db.session.commit()
            flash('Agente creado', "border text-center text-success mb-3")
            return redirect(url_for('home.exito', id=nuevo_agente.id))
        except IntegrityError as e:
            db.session.rollback()
            agente_existente = Agente.query.filter_by(
                dni=nuevo_agente.dni).first()
            if agente_existente is not None:
                error = 'Ya existe un agente con el DNI {} ({} {})'.format(
                    nuevo_agente.dni, agente_existente.nombre,
                    agente_existente.apellido
                )
            else:
                error = e
            flash(error, 'border text-center text-danger mb-3')
    return render_template('preocupacionales/nuevo_agente.html', form=form)


@bp.route('/agente/<int:id>/', methods=('GET', 'POST'))
@login_required
@permission_required(Permiso.EDITAR_AGENTE)
def editar_agente(id):
    agente = Agente.query.filter_by(id=id).first()

    if agente is None:
        abort(404)

    form = FormularioEditarAgente(obj=agente)
    if request.method == 'POST':
        if request.form['action'] == 'guardar':
            if form.validate():
                db.session.add(agente)
                form.populate_obj(agente, edicion=True)
                try:
                    db.session.commit()
                    flash('Los cambios fueron guardados',
                        'border text-center text-success mb-3')
                except IntegrityError as e:
                    db.session.rollback()
                    agente_existente = Agente.query.filter_by(
                        dni=form.dni.data).first()
                    if agente_existente is not None:
                        error = 'Ya existe un agente con el DNI {} ({} {})' \
                            .format(form.dni.data, agente_existente.nombre,
                                agente_existente.apellido)
                        form.dni.errors.append("DNI original: {}".format(
                            agente.dni
                        ))
                    else:
                        error = e
                    flash(error, 'border text-center text-danger mb-3')
        elif request.form['action'] == 'eliminar':
            db.session.delete(agente)
            try:
                db.session.commit()
                flash('Agente eliminado.',
                    'border text-center text-success mb-3')
                return redirect(url_for('preocupacionales.lista'))
            except:
                flash('error sin identificar')

    return render_template('preocupacionales/editar_agente.html', form=form,
        id=id)


@bp.route('/listado')
@bp.route('/listado/<any("completo","pendientes_psi", "pendientes_med"):tipo_listado>')
@login_required
@permission_required(Permiso.VER_AGENTES)
def lista(tipo_listado='completo'):
    if tipo_listado == 'completo':
        agentes = Agente.query.all()
    else:
        from .vistas import AgentesPendientes
        agentes = AgentesPendientes.query.filter(
            AgentesPendientes.tipo_turno == (
                1 if tipo_listado == 'pendientes_psi' else 2
            )
        )
    return render_template('preocupacionales/lista.html', agentes=agentes,
    tipo_listado=tipo_listado)


@bp.route('/cedula/<any("completa","psi","med"):tipo_cedula>/<int:id_agente>/')
@login_required
@permission_required(Permiso.EDITAR_AGENTE)
def cedula(tipo_cedula, id_agente):
    agente = Agente.query.filter_by(id=id_agente).first()

    if agente is None:
        abort(404)

    turno_psi = agente.psi_2.fecha or agente.psi_1.fecha
    turno_med = agente.med_2.fecha or agente.med_1.fecha

    error = None
    if tipo_cedula == 'completa':
        if turno_psi is None or turno_med is None:
            error = ('Falta alguno de los turnos para generar '
            'una cédula completa.')
    elif tipo_cedula == 'psi':
        if turno_psi is None:
            error = ('No puede imprimirse la cédula ya que no hay turno de '
            'preocupacional psicológico asignado para este agente.')
    elif tipo_cedula == 'med':
        if turno_med is None:
            error = ('No puede imprimirse la cédula ya que no hay turnos de '
            'preocupacional clínico asignado para este agente.')
    if error:
        return render_template('error.html', mensaje=error)
    return render_template('preocupacionales/cedula.html', agente=agente,
        tipo_cedula=tipo_cedula, fecha=datetime.now().strftime('%d/%m/%Y'))


@bp.route('/calendario/')
@bp.route('/calendario/<any("psi", "med"):tipo>/')
@login_required
@permission_required(Permiso.VER_AGENTES)
def calendario(tipo='psi'):
    """Vista de calendario

    Esta ruta permite visualizar los turnos en formato de calendario.
    El template incluye botones para elegir turnos psicológicos o médicos.
    La query trae el turno del número más alto de cada tipo para cada agente;
    de este modo si el agente tiene dos turnos asignados, sólo se mostrará el
    segundo, ya que se entiende que si le fue asignado un segundo turno es
    porque no pudo hacerse presente en el primero y, por ende, ese espacio
    queda liberado.
    """
    # obtenemos los turnos, esta consulta equivale a:
    # select id, tipo, max(numero), fecha from turnos where fecha is not null
    # and tipo = (1 o 2 segun psi o med) group by agente_id, tipo
    id_turnos = db.session.query(
        Turno.agente_id, Turno.tipo, func.max(Turno.numero)
    ).filter(
        Turno.fecha != None, Turno.tipo == (1 if tipo == 'psi' else 2)
    ).group_by(Turno.agente_id, Turno.tipo).with_entities(Turno.id).all()
    calendarios = Calendario.query.filter_by(
        tipo = (1 if tipo == 'psi' else 2)).all()
    # query equivalente:
    # select * from turnos where id in (id_turnos)
    turnos = Turno.query.filter(Turno.id.in_([id[0] for id in id_turnos]))
    return render_template('preocupacionales/calendario.html', turnos=turnos,
        tipo=tipo, calendarios=calendarios)
