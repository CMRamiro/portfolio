-- Script para crear la base de datos del portfolio
-- Ejecutar en MySQL antes de usar la aplicación

CREATE DATABASE IF NOT EXISTS portfolio_db
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE portfolio_db;

-- Tabla de usuarios (para el login del administrador)
CREATE TABLE IF NOT EXISTS usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de perfil personal
CREATE TABLE IF NOT EXISTS perfil (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    titulo VARCHAR(100) NOT NULL,
    descripcion TEXT,
    email VARCHAR(120),
    github VARCHAR(200),
    foto VARCHAR(200),
    cv VARCHAR(200)
);

-- Tabla de formación académica (relación: un perfil tiene varias formaciones)
CREATE TABLE IF NOT EXISTS formacion_academica (
    id INT AUTO_INCREMENT PRIMARY KEY,
    institucion VARCHAR(150) NOT NULL,
    carrera VARCHAR(150) NOT NULL,
    ubicacion VARCHAR(100),
    anio_inicio INT,
    anio_fin_estimado INT,
    perfil_id INT,
    CONSTRAINT fk_formacion_perfil FOREIGN KEY (perfil_id)
        REFERENCES perfil(id) ON DELETE CASCADE
);

-- Tabla de tecnologías (relación: un perfil tiene varias tecnologías)
CREATE TABLE IF NOT EXISTS tecnologias (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(80) NOT NULL,
    icono VARCHAR(80),
    aprendiendo BOOLEAN DEFAULT FALSE,
    perfil_id INT,
    CONSTRAINT fk_tecnologia_perfil FOREIGN KEY (perfil_id)
        REFERENCES perfil(id) ON DELETE CASCADE
);

-- Tabla de proyectos (relación: un perfil tiene varios proyectos)
CREATE TABLE IF NOT EXISTS proyectos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    titulo VARCHAR(150) NOT NULL,
    descripcion TEXT,
    url_github VARCHAR(200),
    perfil_id INT,
    CONSTRAINT fk_proyecto_perfil FOREIGN KEY (perfil_id)
        REFERENCES perfil(id) ON DELETE CASCADE
);

-- Tabla de mensajes del formulario de contacto
CREATE TABLE IF NOT EXISTS mensajes_contacto (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(120) NOT NULL,
    mensaje TEXT NOT NULL,
    fecha_envio DATETIME DEFAULT CURRENT_TIMESTAMP
);
