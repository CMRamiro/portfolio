import os
from getpass import getpass

from werkzeug.security import generate_password_hash

from app import create_app
from models import db, Usuario


def main():
    nombre = os.getenv("ADMIN_NOMBRE", "").strip()
    email = os.getenv("ADMIN_EMAIL", "").strip().lower()
    password = os.getenv("ADMIN_PASSWORD", "")

    if not nombre or not email or not password:
        nombre = input("Nombre del administrador: ").strip()
        email = input("Correo electrónico: ").strip().lower()
        password = getpass("Contraseña: ")

    if not nombre or not email or not password:
        print("Debe completar todos los datos.")
        return

    app = create_app()

    with app.app_context():
        if Usuario.query.filter_by(email=email).first():
            print("Ya existe un usuario con ese correo.")
            return

        administrador = Usuario(
            nombre=nombre,
            email=email,
            password_hash=generate_password_hash(password),
            es_admin=True,
        )
        db.session.add(administrador)
        db.session.commit()
        print("Usuario administrador creado correctamente.")


if __name__ == "__main__":
    main()
