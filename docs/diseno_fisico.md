# Diseño físico - Portfolio (MySQL)

- Motor/base: MySQL.
- Base de datos: `portfolio_db` (utf8mb4, utf8mb4_unicode_ci).
- Tipos de datos elegidos según el contenido (VARCHAR para textos cortos, TEXT para descripciones/mensajes, INT para años e identificadores, DATETIME para fechas, BOOLEAN para estado).
- Claves primarias: `id` AUTO_INCREMENT en todas las tablas.
- Claves foráneas: `perfil_id` en `formacion_academica`, `tecnologias` y `proyectos` con `ON DELETE CASCADE`.
- Integridad: campos obligatorios marcados como NOT NULL y `username` como UNIQUE.
- Script de creación: `database/schema.sql`.
