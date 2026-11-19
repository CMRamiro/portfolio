CREATE TABLE IF NOT EXISTS usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(120) NOT NULL,
    email VARCHAR(120) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    es_admin BOOLEAN NOT NULL DEFAULT FALSE,
    fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS perfil (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL UNIQUE,
    nombre_completo VARCHAR(120) NOT NULL,
    titulo VARCHAR(100) NOT NULL,
    presentacion TEXT NOT NULL,
    sobre_mi TEXT NOT NULL,
    objetivo TEXT NOT NULL,
    email VARCHAR(120) NOT NULL,
    github_url VARCHAR(255) NOT NULL,
    ubicacion VARCHAR(150) NOT NULL,
    foto VARCHAR(255) NOT NULL,
    cv_archivo VARCHAR(255) NOT NULL,
    actualizado_en DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT fk_perfil_usuario FOREIGN KEY (usuario_id)
        REFERENCES usuarios(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS formacion_academica (
    id INT AUTO_INCREMENT PRIMARY KEY,
    visible BOOLEAN NOT NULL DEFAULT TRUE,
    orden INT NOT NULL DEFAULT 0,
    fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP,
    institucion VARCHAR(150) NOT NULL,
    titulo VARCHAR(150) NOT NULL,
    descripcion TEXT NOT NULL,
    fecha_inicio VARCHAR(20) NOT NULL,
    fecha_fin VARCHAR(20),
    en_curso BOOLEAN NOT NULL DEFAULT FALSE
);

CREATE TABLE IF NOT EXISTS tecnologias (
    id INT AUTO_INCREMENT PRIMARY KEY,
    visible BOOLEAN NOT NULL DEFAULT TRUE,
    orden INT NOT NULL DEFAULT 0,
    fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP,
    nombre VARCHAR(50) NOT NULL,
    icono VARCHAR(80) NOT NULL,
    estado VARCHAR(30) NOT NULL DEFAULT 'Conocimiento'
);

CREATE TABLE IF NOT EXISTS proyectos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    visible BOOLEAN NOT NULL DEFAULT TRUE,
    orden INT NOT NULL DEFAULT 0,
    fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP,
    titulo VARCHAR(150) NOT NULL,
    descripcion TEXT NOT NULL,
    repositorio_url VARCHAR(255),
    demo_url VARCHAR(255),
    imagen VARCHAR(255),
    destacado BOOLEAN NOT NULL DEFAULT FALSE
);

CREATE TABLE IF NOT EXISTS proyecto_tecnologias (
    proyecto_id INT NOT NULL,
    tecnologia_id INT NOT NULL,
    PRIMARY KEY (proyecto_id, tecnologia_id),
    CONSTRAINT fk_pt_proyecto FOREIGN KEY (proyecto_id)
        REFERENCES proyectos(id) ON DELETE CASCADE,
    CONSTRAINT fk_pt_tecnologia FOREIGN KEY (tecnologia_id)
        REFERENCES tecnologias(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS mensajes_contacto (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(120) NOT NULL,
    asunto VARCHAR(150) NOT NULL,
    mensaje TEXT NOT NULL,
    leido BOOLEAN NOT NULL DEFAULT FALSE,
    fecha_envio DATETIME DEFAULT CURRENT_TIMESTAMP
);
