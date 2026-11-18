# Diseño lógico - Portfolio

Tablas y campos:

## usuarios
- id (INT, PK, AUTO_INCREMENT)
- username (VARCHAR(50), UNIQUE, NOT NULL)
- password_hash (VARCHAR(255), NOT NULL)
- fecha_creacion (DATETIME)

## perfil
- id (INT, PK, AUTO_INCREMENT)
- nombre (VARCHAR(100), NOT NULL)
- titulo (VARCHAR(100), NOT NULL)
- descripcion (TEXT)
- email (VARCHAR(120))
- github (VARCHAR(200))
- foto (VARCHAR(200))
- cv (VARCHAR(200))

## formacion_academica
- id (INT, PK, AUTO_INCREMENT)
- institucion (VARCHAR(150), NOT NULL)
- carrera (VARCHAR(150), NOT NULL)
- ubicacion (VARCHAR(100))
- anio_inicio (INT)
- anio_fin_estimado (INT)
- perfil_id (INT, FK -> perfil.id)

## tecnologias
- id (INT, PK, AUTO_INCREMENT)
- nombre (VARCHAR(80), NOT NULL)
- icono (VARCHAR(80))
- aprendiendo (BOOLEAN)
- perfil_id (INT, FK -> perfil.id)

## proyectos
- id (INT, PK, AUTO_INCREMENT)
- titulo (VARCHAR(150), NOT NULL)
- descripcion (TEXT)
- url_github (VARCHAR(200))
- perfil_id (INT, FK -> perfil.id)

## mensajes_contacto
- id (INT, PK, AUTO_INCREMENT)
- nombre (VARCHAR(100), NOT NULL)
- email (VARCHAR(120), NOT NULL)
- mensaje (TEXT, NOT NULL)
- fecha_envio (DATETIME)
