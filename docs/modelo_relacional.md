# Modelo relacional - Portfolio

Entidades y relaciones principales:

- **perfil**: guarda los datos personales y de presentación.
- **formacion_academica**: pertenece a un perfil (N a 1).
- **tecnologias**: pertenece a un perfil (N a 1).
- **proyectos**: pertenece a un perfil (N a 1).
- **usuarios**: usuario administrador para el panel privado.
- **mensajes_contacto**: mensajes enviados desde el formulario público.

Relaciones:
- Un `perfil` puede tener muchas `formacion_academica`.
- Un `perfil` puede tener muchas `tecnologias`.
- Un `perfil` puede tener muchos `proyectos`.
- `mensajes_contacto` y `usuarios` no dependen del perfil (tablas independientes).

Claves:
- Cada tabla tiene su clave primaria `id`.
- Las tablas `formacion_academica`, `tecnologias` y `proyectos` tienen clave foránea `perfil_id` que referencia a `perfil(id)`.
