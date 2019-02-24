from flask import (
    Blueprint, redirect, url_for, render_template, request
)
from flask_login import (
    current_user, login_user, logout_user
)
from werkzeug.urls import url_parse
from .formularios import FormularioLogin, FormularioRegistro
from .modelos import db, Usuario

bp = Blueprint('auth', __name__, url_prefix='')

@bp.route('/login/', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home.index'))
    form = FormularioLogin()
    if form.validate_on_submit():
        usuario = Usuario.query.filter_by(usuario=form.usuario.data).first()
        if usuario is None or not usuario.check_password(form.password.data):
            flash('Usuario o contraseña inválidos',
                'border text-center text-danger mb-3')
            return redirect(url_for('auth.login'))
        login_user(usuario, remember=form.recordarme.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('home.index')
        return redirect(next_page)
    return render_template('auth/login.html', title='Ingresar', form=form)

@bp.route('/logout/')
def logout():
    logout_user()
    return redirect(url_for('home.index'))

@bp.route('/registro/', methods=['GET', 'POST'])
def registro():
    form = FormularioRegistro()
    if form.validate_on_submit():
        usuario = Usuario(usuario=form.usuario.data)
        usuario.set_password(form.password.data)
        db.session.add(usuario)
        db.session.commit()
        flash('Se ha generado el usuario {}'.format(form.usuario.data),
            'border text-center text-success mb-3')
        return redirect(url_for('home.index'))
    return render_template('auth/registro.html', title='Registro', form=form)
