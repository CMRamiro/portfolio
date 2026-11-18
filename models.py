
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()


class Usuario(UserMixin, db.Model):
    __tablename__ = "usuarios"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    es_admin = db.Column(db.Boolean, default=False, nullable=False)
    fecha_creacion = db.Column(
        db.DateTime,
        server_default=db.func.current_timestamp()
    )


class Perfil(db.Model):
    __tablename__ = "perfil"

    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, nullable=False, unique=True)
    nombre_completo = db.Column(db.String(120), nullable=False)
    titulo = db.Column(db.String(100), nullable=False)
    presentacion = db.Column(db.Text, nullable=False)
    sobre_mi = db.Column(db.Text, nullable=False)
    objetivo = db.Column(db.Text, nullable=False)
    email = db.Column(db.String(120), nullable=False)
    github_url = db.Column(db.String(255), nullable=False)
    ubicacion = db.Column(db.String(150), nullable=False)
    foto = db.Column(db.String(255), nullable=False)
    cv_archivo = db.Column(db.String(255), nullable=False)
    actualizado_en = db.Column(
        db.DateTime,
        server_default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp(),
        nullable=False
    )


class FormacionAcademica(db.Model):
    __tablename__ = "formacion_academica"

    id = db.Column(db.Integer, primary_key=True)
    visible = db.Column(db.Boolean, nullable=False, default=True)
    orden = db.Column(db.Integer, nullable=False, default=0)
    fecha_creacion = db.Column(
        db.DateTime,
        server_default=db.func.current_timestamp()
    )
    institucion = db.Column(db.String(150), nullable=False)
    titulo = db.Column(db.String(150), nullable=False)
    descripcion = db.Column(db.Text, nullable=False)
    fecha_inicio = db.Column(db.String(20), nullable=False)
    fecha_fin = db.Column(db.String(20))
    en_curso = db.Column(db.Boolean, nullable=False, default=False)


class Tecnologia(db.Model):
    __tablename__ = "tecnologias"

    id = db.Column(db.Integer, primary_key=True)
    visible = db.Column(db.Boolean, nullable=False, default=True)
    orden = db.Column(db.Integer, nullable=False, default=0)
    fecha_creacion = db.Column(
        db.DateTime,
        server_default=db.func.current_timestamp()
    )
    nombre = db.Column(db.String(50), nullable=False)
    icono = db.Column(db.String(80), nullable=False)
    estado = db.Column(db.String(30), nullable=False, default="Conocimiento")


class Proyecto(db.Model):
    __tablename__ = "proyectos"

    id = db.Column(db.Integer, primary_key=True)
    visible = db.Column(db.Boolean, nullable=False, default=True)
    orden = db.Column(db.Integer, nullable=False, default=0)
    fecha_creacion = db.Column(
        db.DateTime,
        server_default=db.func.current_timestamp()
    )
    titulo = db.Column(db.String(150), nullable=False)
    descripcion = db.Column(db.Text, nullable=False)
    repositorio_url = db.Column(db.String(255))
    demo_url = db.Column(db.String(255))
    imagen = db.Column(db.String(255))
    destacado = db.Column(db.Boolean, nullable=False, default=False)

    tecnologias = db.relationship(
        "Tecnologia",
        secondary="proyecto_tecnologias",
        backref="proyectos"
    )


class ProyectoTecnologia(db.Model):
    __tablename__ = "proyecto_tecnologias"

    proyecto_id = db.Column(
        db.Integer,
        db.ForeignKey("proyectos.id"),
        primary_key=True
    )
    tecnologia_id = db.Column(
        db.Integer,
        db.ForeignKey("tecnologias.id"),
        primary_key=True
    )



class MensajeContacto(db.Model):
    __tablename__ = "mensajes_contacto"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    asunto = db.Column(db.String(150), nullable=False)
    mensaje = db.Column(db.Text, nullable=False)
    leido = db.Column(db.Boolean, nullable=False, default=False)
    fecha_envio = db.Column(
        db.DateTime,
        server_default=db.func.current_timestamp(),
        nullable=False
    )
