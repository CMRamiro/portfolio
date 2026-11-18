"""
Formularios del proyecto usando Flask-WTF.
Incluye formularios públicos y de administración.
"""

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SubmitField, BooleanField, IntegerField
from wtforms.validators import DataRequired, Email, Length, Optional


class LoginForm(FlaskForm):
    """Formulario de inicio de sesión para el administrador."""

    username = StringField("Usuario", validators=[DataRequired(), Length(max=50)])
    password = PasswordField("Contraseña", validators=[DataRequired()])
    submit = SubmitField("Ingresar")


class ContactoForm(FlaskForm):
    """Formulario de contacto público."""

    nombre = StringField("Nombre", validators=[DataRequired(), Length(max=100)])
    email = StringField("Correo electrónico", validators=[DataRequired(), Email(), Length(max=120)])
    mensaje = TextAreaField("Mensaje", validators=[DataRequired()])
    submit = SubmitField("Enviar")


class PerfilForm(FlaskForm):
    """Formulario para editar la información del perfil."""

    nombre = StringField("Nombre", validators=[DataRequired(), Length(max=100)])
    titulo = StringField("Título", validators=[DataRequired(), Length(max=100)])
    descripcion = TextAreaField("Descripción", validators=[Optional()])
    email = StringField("Correo", validators=[Optional(), Email(), Length(max=120)])
    github = StringField("GitHub", validators=[Optional(), Length(max=200)])
    foto = StringField("Foto (nombre del archivo en static/img)", validators=[Optional(), Length(max=200)])
    cv = StringField("CV (nombre del archivo en static/docs)", validators=[Optional(), Length(max=200)])
    submit = SubmitField("Guardar")


class TecnologiaForm(FlaskForm):
    """Formulario para gestionar tecnologías."""

    nombre = StringField("Nombre", validators=[DataRequired(), Length(max=80)])
    icono = StringField("Icono (clase FontAwesome)", validators=[Optional(), Length(max=80)])
    aprendiendo = BooleanField("Estoy aprendiendo esta tecnología")
    submit = SubmitField("Guardar")


class ProyectoForm(FlaskForm):
    """Formulario para gestionar proyectos."""

    titulo = StringField("Título", validators=[DataRequired(), Length(max=150)])
    descripcion = TextAreaField("Descripción", validators=[Optional()])
    url_github = StringField("URL de GitHub", validators=[Optional(), Length(max=200)])
    submit = SubmitField("Guardar")


class FormacionForm(FlaskForm):
    """Formulario para gestionar formación académica."""

    institucion = StringField("Institución", validators=[DataRequired(), Length(max=150)])
    carrera = StringField("Carrera", validators=[DataRequired(), Length(max=150)])
    ubicacion = StringField("Ubicación", validators=[Optional(), Length(max=100)])
    anio_inicio = IntegerField("Año de inicio", validators=[Optional()])
    anio_fin_estimado = IntegerField("Año de finalización estimado", validators=[Optional()])
    submit = SubmitField("Guardar")
