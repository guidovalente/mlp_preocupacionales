from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, EqualTo, ValidationError
from .modelos import Usuario

class FormularioLogin(FlaskForm):
    """Formulario de login
    """
    usuario = StringField('Usuario', validators=[DataRequired()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    recordarme = BooleanField('Recordarme')
    enviar = SubmitField('Ingresar')

class FormularioRegistro(FlaskForm):
    usuario = StringField('Usuario', validators=[DataRequired()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    password2 = PasswordField('Repita la contraseña', validators=[
        DataRequired(), EqualTo('password')])
    registrarse = SubmitField('Registrar')

    def validate_usuario(self, usuario):
        usuario = Usuario.query.filter_by(usuario=usuario.data).first()
        if usuario is not None:
            raise ValidationError('El nombre de usuario ya está en uso.')
