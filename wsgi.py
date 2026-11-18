"""
Archivo de entrada para servidores WSGI (por ejemplo PythonAnywhere).
"""

from app import create_app

application = create_app()
