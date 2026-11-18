"""
Rutas principales de la aplicación.
Incluye vistas públicas, formulario de contacto, login y panel de administración.
"""

from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash
from models import db, Usuario, Perfil, FormacionAcademica, Tecnologia, Proyecto, MensajeContacto
from forms import (
    LoginForm, ContactoForm, PerfilForm, TecnologiaForm,
    ProyectoForm, FormacionForm
)

main_bp = Blueprint("main", __name__)


@main_bp.route("/", methods=["GET", "POST"])
def index():
    """Página principal del portfolio (contenido público)."""
    form_contacto = ContactoForm()

    # Si se envía el formulario de contacto, se guarda el mensaje en la base de datos
    if form_contacto.validate_on_submit():
        nuevo_mensaje = MensajeContacto(
            nombre=form_contacto.nombre.data,
            email=form_contacto.email.data,
            mensaje=form_contacto.mensaje.data
        )
        try:
            db.session.add(nuevo_mensaje)
            db.session.commit()
            flash("Mensaje enviado correctamente.", "success")
        except Exception:
            db.session.rollback()
            flash("Ocurrió un error al enviar el mensaje.", "error")
        return redirect(url_for("main.index") + "#contacto")

    # Se obtienen los datos desde la base de datos (si existen)
    perfil = Perfil.query.first()
    formaciones = FormacionAcademica.query.all()
    tecnologias = Tecnologia.query.all()
    proyectos = Proyecto.query.all()

    return render_template(
        "index.html",
        form_contacto=form_contacto,
        perfil=perfil,
        formaciones=formaciones,
        tecnologias=tecnologias,
        proyectos=proyectos
    )


@main_bp.route("/login", methods=["GET", "POST"])
def login():
    """Inicio de sesión del administrador."""
    if current_user.is_authenticated:
        return redirect(url_for("main.admin"))

    form = LoginForm()
    if form.validate_on_submit():
        usuario = Usuario.query.filter_by(username=form.username.data).first()
        # Se verifica la contraseña usando hash seguro
        if usuario and check_password_hash(usuario.password_hash, form.password.data):
            login_user(usuario)
            return redirect(url_for("main.admin"))
        else:
            flash("Usuario o contraseña incorrectos.", "error")

    return render_template("login.html", form=form)


@main_bp.route("/logout")
@login_required
def logout():
    """Cierra la sesión del administrador."""
    logout_user()
    return redirect(url_for("main.index"))


@main_bp.route("/admin")
@login_required
def admin():
    """Panel de administración privado."""
    perfil = Perfil.query.first()
    formaciones = FormacionAcademica.query.all()
    tecnologias = Tecnologia.query.all()
    proyectos = Proyecto.query.all()
    mensajes = MensajeContacto.query.order_by(MensajeContacto.fecha_envio.desc()).all()
    return render_template(
        "admin.html",
        perfil=perfil,
        formaciones=formaciones,
        tecnologias=tecnologias,
        proyectos=proyectos,
        mensajes=mensajes
    )


@main_bp.route("/admin/perfil", methods=["GET", "POST"])
@login_required
def admin_perfil():
    """Crear o editar la información del perfil."""
    perfil = Perfil.query.first()
    form = PerfilForm(obj=perfil)

    if form.validate_on_submit():
        if not perfil:
            perfil = Perfil()
            db.session.add(perfil)
        form.populate_obj(perfil)
        db.session.commit()
        flash("Perfil guardado correctamente.", "success")
        return redirect(url_for("main.admin"))

    return render_template("admin_perfil.html", form=form, perfil=perfil)


@main_bp.route("/admin/tecnologias", methods=["GET", "POST"])
@login_required
def admin_tecnologias():
    """Agregar una nueva tecnología."""
    form = TecnologiaForm()
    if form.validate_on_submit():
        perfil = Perfil.query.first()
        tecnologia = Tecnologia(
            nombre=form.nombre.data,
            icono=form.icono.data,
            aprendiendo=form.aprendiendo.data,
            perfil_id=perfil.id if perfil else None
        )
        db.session.add(tecnologia)
        db.session.commit()
        flash("Tecnología agregada.", "success")
        return redirect(url_for("main.admin"))
    return render_template("admin_form.html", form=form, titulo="Agregar tecnología")


@main_bp.route("/admin/tecnologias/<int:id>/eliminar", methods=["POST"])
@login_required
def eliminar_tecnologia(id):
    tecnologia = Tecnologia.query.get_or_404(id)
    db.session.delete(tecnologia)
    db.session.commit()
    flash("Tecnología eliminada.", "success")
    return redirect(url_for("main.admin"))


@main_bp.route("/admin/proyectos", methods=["GET", "POST"])
@login_required
def admin_proyectos():
    """Agregar un nuevo proyecto."""
    form = ProyectoForm()
    if form.validate_on_submit():
        perfil = Perfil.query.first()
        proyecto = Proyecto(
            titulo=form.titulo.data,
            descripcion=form.descripcion.data,
            url_github=form.url_github.data,
            perfil_id=perfil.id if perfil else None
        )
        db.session.add(proyecto)
        db.session.commit()
        flash("Proyecto agregado.", "success")
        return redirect(url_for("main.admin"))
    return render_template("admin_form.html", form=form, titulo="Agregar proyecto")


@main_bp.route("/admin/proyectos/<int:id>/eliminar", methods=["POST"])
@login_required
def eliminar_proyecto(id):
    proyecto = Proyecto.query.get_or_404(id)
    db.session.delete(proyecto)
    db.session.commit()
    flash("Proyecto eliminado.", "success")
    return redirect(url_for("main.admin"))


@main_bp.route("/admin/formacion", methods=["GET", "POST"])
@login_required
def admin_formacion():
    """Agregar formación académica."""
    form = FormacionForm()
    if form.validate_on_submit():
        perfil = Perfil.query.first()
        formacion = FormacionAcademica(
            institucion=form.institucion.data,
            carrera=form.carrera.data,
            ubicacion=form.ubicacion.data,
            anio_inicio=form.anio_inicio.data,
            anio_fin_estimado=form.anio_fin_estimado.data,
            perfil_id=perfil.id if perfil else None
        )
        db.session.add(formacion)
        db.session.commit()
        flash("Formación agregada.", "success")
        return redirect(url_for("main.admin"))
    return render_template("admin_form.html", form=form, titulo="Agregar formación")


@main_bp.route("/admin/formacion/<int:id>/eliminar", methods=["POST"])
@login_required
def eliminar_formacion(id):
    formacion = FormacionAcademica.query.get_or_404(id)
    db.session.delete(formacion)
    db.session.commit()
    flash("Formación eliminada.", "success")
    return redirect(url_for("main.admin"))
