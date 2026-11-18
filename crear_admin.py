

from getpass import getpass
from werkzeug.security import generate_password_hash

from app import create_app
from models import db, Usuario


def main():
    app = create_app()

    with app.app_context():
        username = input("Nombre de usuario administrador: ").strip()
        password = getpass("Contraseña: ")

        if not username or not password:
            print("Debe completar usuario y contraseña.")
            return

        if Usuario.query.filter_by(username=username).first():
            print("Ya existe un usuario con ese nombre.")
            return

        # Se guarda la contraseña como hash seguro, nunca en texto plano
        nuevo_usuario = Usuario(
            username=username,
            password_hash=generate_password_hash(password)
        )
        db.session.add(nuevo_usuario)
        db.session.commit()
        print("Usuario administrador creado correctamente.")


if __name__ == "__main__":
    main()
