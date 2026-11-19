from functools import wraps

from flask import Blueprint, abort, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from sqlalchemy import or_
from werkzeug.security import check_password_hash, generate_password_hash

from forms import (
    AdminCuentaForm,
    ContactoForm,
    FormacionForm,
    LoginForm,
    PerfilForm,
    ProyectoForm,
    TecnologiaForm,
)
from models import (
    db,
    Usuario,
    Perfil,
    FormacionAcademica,
    Tecnologia,
    Proyecto,
    MensajeContacto,
)

main_bp = Blueprint("main", __name__)


def admin_required(view):
    @wraps(view)
    @login_required
    def wrapped(*args, **kwargs):
        if not current_user.es_admin:
            abort(403)
        return view(*args, **kwargs)

    return wrapped


def valor_texto(valor):
    return valor or ""


def guardar(mensaje):
    try:
        db.session.commit()
        flash(mensaje, "success")
    except Exception:
        db.session.rollback()
        flash("No se pudo guardar el cambio. Inténtalo nuevamente.", "error")


@main_bp.route("/", methods=["GET", "POST"])
def index():
    form_contacto = ContactoForm()

    if form_contacto.validate_on_submit():
        mensaje = MensajeContacto(
            nombre=form_contacto.nombre.data,
            email=form_contacto.email.data,
            asunto=valor_texto(form_contacto.asunto.data) or "Consulta desde el portfolio",
            mensaje=form_contacto.mensaje.data,
        )
        try:
            db.session.add(mensaje)
            db.session.commit()
            flash("Mensaje enviado correctamente.", "success")
        except Exception:
            db.session.rollback()
            flash("Ocurrió un error al enviar el mensaje.", "error")
        return redirect(url_for("main.index") + "#contacto")

    perfil = Perfil.query.first()
    formaciones = (
        FormacionAcademica.query.filter_by(visible=True)
        .order_by(FormacionAcademica.orden, FormacionAcademica.id)
        .all()
    )
    tecnologias = (
        Tecnologia.query.filter_by(visible=True)
        .order_by(Tecnologia.orden, Tecnologia.id)
        .all()
    )
    proyectos = (
        Proyecto.query.filter_by(visible=True)
        .order_by(Proyecto.orden, Proyecto.id)
        .all()
    )

    return render_template(
        "index.html",
        form_contacto=form_contacto,
        perfil=perfil,
        formaciones=formaciones,
        tecnologias=tecnologias,
        proyectos=proyectos,
    )


@main_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.admin"))

    form = LoginForm()
    if form.validate_on_submit():
        identificador = (form.usuario.data or "").strip()
        usuario = Usuario.query.filter(
            or_(Usuario.nombre == identificador, Usuario.email == identificador)
        ).first()
        if usuario and usuario.es_admin and check_password_hash(
            usuario.password_hash, form.password.data
        ):
            login_user(usuario)
            return redirect(url_for("main.admin"))
        flash("Usuario o contraseña incorrectos.", "error")

    return render_template("login.html", form=form)


@main_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.index"))


@main_bp.route("/admin")
@admin_required
def admin():
    return render_template(
        "admin.html",
        perfil=Perfil.query.first(),
        formaciones=FormacionAcademica.query.order_by(
            FormacionAcademica.orden, FormacionAcademica.id
        ).all(),
        tecnologias=Tecnologia.query.order_by(Tecnologia.orden, Tecnologia.id).all(),
        proyectos=Proyecto.query.order_by(Proyecto.orden, Proyecto.id).all(),
        mensajes=MensajeContacto.query.order_by(
            MensajeContacto.fecha_envio.desc()
        ).all(),
    )


@main_bp.route("/admin/perfil", methods=["GET", "POST"])
@admin_required
def admin_perfil():
    perfil = Perfil.query.first()
    form = PerfilForm(obj=perfil)

    if form.validate_on_submit():
        if perfil is None:
            perfil = Perfil(usuario_id=current_user.id)
            db.session.add(perfil)
        form.populate_obj(perfil)
        for campo in (
            "presentacion",
            "sobre_mi",
            "objetivo",
            "github_url",
            "ubicacion",
            "foto",
            "cv_archivo",
        ):
            setattr(perfil, campo, valor_texto(getattr(perfil, campo)))
        guardar("Perfil guardado correctamente.")
        return redirect(url_for("main.admin"))

    return render_template("admin_perfil.html", form=form, perfil=perfil)


@main_bp.route("/admin/cuenta", methods=["GET", "POST"])
@admin_required
def admin_cuenta():
    usuario = db.session.get(Usuario, current_user.id) or abort(404)
    form = AdminCuentaForm(obj=usuario)

    if form.validate_on_submit():
        email = (form.email.data or "").strip().lower()
        otro_usuario = Usuario.query.filter(
            Usuario.email == email, Usuario.id != usuario.id
        ).first()
        if otro_usuario:
            form.email.errors.append("Ya existe un usuario con ese correo.")
        else:
            usuario.nombre = (form.nombre.data or "").strip()
            usuario.email = email
            if form.password.data:
                usuario.password_hash = generate_password_hash(form.password.data)
            guardar("Datos de acceso actualizados.")
            return redirect(url_for("main.admin"))

    return render_template("admin_cuenta.html", form=form)


@main_bp.route("/admin/tecnologias/nueva", methods=["GET", "POST"])
@main_bp.route("/admin/tecnologias/<int:id>/editar", methods=["GET", "POST"])
@admin_required
def admin_tecnologia(id=None):
    tecnologia = db.session.get(Tecnologia, id) if id is not None else Tecnologia()
    form = TecnologiaForm(obj=tecnologia)

    if form.validate_on_submit():
        form.populate_obj(tecnologia)
        tecnologia.orden = form.orden.data or 0
        if id is None:
            db.session.add(tecnologia)
        guardar("Tecnología guardada." if id is not None else "Tecnología agregada.")
        return redirect(url_for("main.admin"))

    return render_template(
        "admin_form.html",
        form=form,
        titulo="Editar tecnología" if id is not None else "Agregar tecnología",
    )


@main_bp.route("/admin/tecnologias/<int:id>/eliminar", methods=["POST"])
@admin_required
def eliminar_tecnologia(id):
    tecnologia = db.session.get(Tecnologia, id) or abort(404)
    db.session.delete(tecnologia)
    guardar("Tecnología eliminada.")
    return redirect(url_for("main.admin"))


@main_bp.route("/admin/proyectos/nuevo", methods=["GET", "POST"])
@main_bp.route("/admin/proyectos/<int:id>/editar", methods=["GET", "POST"])
@admin_required
def admin_proyecto(id=None):
    proyecto = db.session.get(Proyecto, id) if id is not None else Proyecto()
    form = ProyectoForm(obj=proyecto)
    form.tecnologias.choices = [
        (t.id, t.nombre) for t in Tecnologia.query.order_by(Tecnologia.nombre).all()
    ]
    if request.method == "GET" and id is not None:
        form.tecnologias.data = [t.id for t in proyecto.tecnologias]

    if form.validate_on_submit():
        proyecto.titulo = form.titulo.data
        proyecto.descripcion = valor_texto(form.descripcion.data)
        proyecto.repositorio_url = valor_texto(form.repositorio_url.data)
        proyecto.demo_url = valor_texto(form.demo_url.data)
        proyecto.imagen = valor_texto(form.imagen.data)
        proyecto.destacado = form.destacado.data
        proyecto.visible = form.visible.data
        proyecto.orden = form.orden.data or 0
        proyecto.tecnologias = [
            tecnologia
            for tecnologia in (
                db.session.get(Tecnologia, tecnologia_id)
                for tecnologia_id in form.tecnologias.data
            )
            if tecnologia is not None
        ]
        proyecto.orden = form.orden.data or 0
        for campo in ("descripcion", "repositorio_url", "demo_url", "imagen"):
            setattr(proyecto, campo, valor_texto(getattr(proyecto, campo)))
        if id is None:
            db.session.add(proyecto)
        guardar("Proyecto guardado." if id is not None else "Proyecto agregado.")
        return redirect(url_for("main.admin"))

    return render_template(
        "admin_form.html",
        form=form,
        titulo="Editar proyecto" if id is not None else "Agregar proyecto",
    )


@main_bp.route("/admin/proyectos/<int:id>/eliminar", methods=["POST"])
@admin_required
def eliminar_proyecto(id):
    proyecto = db.session.get(Proyecto, id) or abort(404)
    db.session.delete(proyecto)
    guardar("Proyecto eliminado.")
    return redirect(url_for("main.admin"))


@main_bp.route("/admin/formacion/nueva", methods=["GET", "POST"])
@main_bp.route("/admin/formacion/<int:id>/editar", methods=["GET", "POST"])
@admin_required
def admin_formacion(id=None):
    formacion = (
        db.session.get(FormacionAcademica, id) if id is not None else FormacionAcademica()
    )
    form = FormacionForm(obj=formacion)

    if form.validate_on_submit():
        form.populate_obj(formacion)
        formacion.orden = form.orden.data or 0
        for campo in ("descripcion", "fecha_inicio", "fecha_fin"):
            setattr(formacion, campo, valor_texto(getattr(formacion, campo)))
        if id is None:
            db.session.add(formacion)
        guardar("Formación guardada." if id is not None else "Formación agregada.")
        return redirect(url_for("main.admin"))

    return render_template(
        "admin_form.html",
        form=form,
        titulo="Editar formación" if id is not None else "Agregar formación",
    )


@main_bp.route("/admin/formacion/<int:id>/eliminar", methods=["POST"])
@admin_required
def eliminar_formacion(id):
    formacion = db.session.get(FormacionAcademica, id) or abort(404)
    db.session.delete(formacion)
    guardar("Formación eliminada.")
    return redirect(url_for("main.admin"))


@main_bp.route("/admin/<seccion>/<int:id>/visibilidad", methods=["POST"])
@admin_required
def alternar_visibilidad(seccion, id):
    modelos = {
        "tecnologias": Tecnologia,
        "proyectos": Proyecto,
        "formacion": FormacionAcademica,
    }
    modelo = modelos.get(seccion) or abort(404)
    elemento = db.session.get(modelo, id) or abort(404)
    elemento.visible = not elemento.visible
    guardar("Visibilidad actualizada.")
    return redirect(url_for("main.admin"))


@main_bp.route("/admin/mensajes/<int:id>/leido", methods=["POST"])
@admin_required
def alternar_leido(id):
    mensaje = db.session.get(MensajeContacto, id) or abort(404)
    mensaje.leido = not mensaje.leido
    guardar("Estado del mensaje actualizado.")
    return redirect(url_for("main.admin"))


@main_bp.route("/admin/mensajes/<int:id>/eliminar", methods=["POST"])
@admin_required
def eliminar_mensaje(id):
    mensaje = db.session.get(MensajeContacto, id) or abort(404)
    db.session.delete(mensaje)
    guardar("Mensaje eliminado.")
    return redirect(url_for("main.admin"))
