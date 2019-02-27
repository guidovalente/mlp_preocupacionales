from app.modelo_base import db, Base
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class Usuario(UserMixin, Base):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    usuario = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    rol_id = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=False)

    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)
        if self.rol is None:
            self.rol = Rol.query.filter_by(default=True).first()

    def __repr__(self):
        return "<Usuario {}>".format(self.usuario)

    def set_password(self, password):
        assert password is not None
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def can(self, permission):
        return self.rol is not None and self.rol.tiene_permiso(permission)


class Rol(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(32), unique=True)
    default = db.Column(db.Boolean, default=False, index=True)
    permisos = db.Column(db.Integer)
    usuarios = db.relationship('Usuario', backref='rol', lazy='dynamic')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self.permisos is None:
            self.permisos = 0

    def __repr__(self):
        return "<Rol {}>".format(self.nombre)

    def agregar_permisos(self, *permisos):
        """Método para asignar permisos a un rol

        Se pueden pasar uno o más permisos a la vez para asignar.
        """
        for permiso in permisos:
            if not self.tiene_permiso(permiso):
                self.permisos += permiso

    def quitar_permisos(self, *permisos):
        """Método para quitar permisos a un rol

        Se pueden pasar uno o más permisos a la vez para quitar.
        """
        for permiso in permisos:
            if self.tiene_permiso(permiso):
                self.permisos -= permiso

    def reiniciar_permisos(self):
        """Método para reiniciar los permisos

        Al invocarse este método los permisos de la instancia de esta
        clase se vuelven a 0 (sin permisos).
        """
        self.permisos = 0

    def tiene_permiso(self, permiso):
        """Método para verificar si un rol tiene un permiso
        """
        return self.permisos & permiso == permiso

    @staticmethod
    def insertar_roles():
        """Método estático para insertar roles en la base de datos
        """
        roles = {
            'CARGA_AGENTES': [
                Permiso.VER_AGENTES,
                Permiso.CREAR_AGENTE
            ],
            'EDITA_AGENTES': [
                Permiso.VER_AGENTES,
                Permiso.CREAR_AGENTE,
                Permiso.EDITAR_AGENTE
            ],
            'ADMIN': [
                Permiso.VER_AGENTES,
                Permiso.CREAR_AGENTE,
                Permiso.EDITAR_AGENTE,
                Permiso.ADMIN
            ]
        }
        rol_por_defecto = 'CARGA_AGENTES'
        for r in roles:
            rol = Rol.query.filter_by(nombre=r).first()
            if rol is None:
                rol = Rol(nombre=r)
            rol.reiniciar_permisos()
            rol.agregar_permisos(*roles[r])
            rol.default = (rol.nombre == rol_por_defecto)
            db.session.add(rol)
        db.session.commit()

class Permiso():
    VER_AGENTES = 1
    CREAR_AGENTE = 2
    EDITAR_AGENTE = 4
    ADMIN = 8
