from flask_wtf import FlaskForm
from wtforms import (
    BooleanField,
    IntegerField,
    PasswordField,
    SelectField,
    SelectMultipleField,
    StringField,
    SubmitField,
    TextAreaField,
)
from wtforms.validators import DataRequired, Email, Length, NumberRange, Optional

ESTADOS_TECNOLOGIA = [
    ("Conocimiento", "Conocimiento"),
    ("Intermedio", "Intermedio"),
    ("Avanzado", "Avanzado"),
    ("Aprendiendo", "Aprendiendo"),
]


class LoginForm(FlaskForm):
    usuario = StringField("Usuario o correo", validators=[DataRequired(), Length(max=120)])
    password = PasswordField("Contraseña", validators=[DataRequired()])
    submit = SubmitField("Ingresar")


class ContactoForm(FlaskForm):
    nombre = StringField("Nombre", validators=[DataRequired(), Length(max=100)])
    email = StringField("Correo electrónico", validators=[DataRequired(), Email(), Length(max=120)])
    asunto = StringField("Asunto", validators=[Optional(), Length(max=150)])
    mensaje = TextAreaField("Mensaje", validators=[DataRequired()])
    submit = SubmitField("Enviar")


class PerfilForm(FlaskForm):
    nombre_completo = StringField("Nombre completo", validators=[DataRequired(), Length(max=120)])
    titulo = StringField("Título", validators=[DataRequired(), Length(max=100)])
    presentacion = TextAreaField("Presentación", validators=[Optional()])
    sobre_mi = TextAreaField("Sobre mí", validators=[Optional()])
    objetivo = TextAreaField("Objetivo", validators=[Optional()])
    email = StringField("Correo", validators=[DataRequired(), Email(), Length(max=120)])
    github_url = StringField("GitHub", validators=[Optional(), Length(max=255)])
    ubicacion = StringField("Ubicación", validators=[Optional(), Length(max=150)])
    foto = StringField("Foto (archivo en static/img)", validators=[Optional(), Length(max=255)])
    cv_archivo = StringField("CV (archivo en static/docs)", validators=[Optional(), Length(max=255)])
    submit = SubmitField("Guardar")


class TecnologiaForm(FlaskForm):
    nombre = StringField("Nombre", validators=[DataRequired(), Length(max=50)])
    icono = StringField("Icono (clase FontAwesome)", validators=[Optional(), Length(max=80)])
    estado = SelectField("Estado", choices=ESTADOS_TECNOLOGIA, default="Conocimiento")
    visible = BooleanField("Visible en la página", default=True)
    orden = IntegerField("Orden", default=0, validators=[NumberRange(min=0)])
    submit = SubmitField("Guardar")


class ProyectoForm(FlaskForm):
    titulo = StringField("Título", validators=[DataRequired(), Length(max=150)])
    descripcion = TextAreaField("Descripción", validators=[Optional()])
    repositorio_url = StringField("URL del repositorio", validators=[Optional(), Length(max=255)])
    demo_url = StringField("URL de la demo", validators=[Optional(), Length(max=255)])
    imagen = StringField("Imagen (archivo en static/img)", validators=[Optional(), Length(max=255)])
    destacado = BooleanField("Destacado")
    visible = BooleanField("Visible en la página", default=True)
    orden = IntegerField("Orden", default=0, validators=[NumberRange(min=0)])
    tecnologias = SelectMultipleField("Tecnologías", coerce=int, choices=[], validators=[Optional()])
    submit = SubmitField("Guardar")


class FormacionForm(FlaskForm):
    institucion = StringField("Institución", validators=[DataRequired(), Length(max=150)])
    titulo = StringField("Título", validators=[DataRequired(), Length(max=150)])
    descripcion = TextAreaField("Descripción", validators=[Optional()])
    fecha_inicio = StringField("Fecha de inicio", validators=[Optional(), Length(max=20)])
    fecha_fin = StringField("Fecha de finalización", validators=[Optional(), Length(max=20)])
    en_curso = BooleanField("En curso")
    visible = BooleanField("Visible en la página", default=True)
    orden = IntegerField("Orden", default=0, validators=[NumberRange(min=0)])
    submit = SubmitField("Guardar")
