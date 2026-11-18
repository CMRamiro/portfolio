-- Datos iniciales de ejemplo para el portfolio
-- Ejecutar después de database/schema.sql

USE portfolio_db;

-- Perfil personal
INSERT INTO perfil (nombre, titulo, descripcion, email, github, foto, cv)
VALUES (
  'Michael Ramiro Cáceres',
  'Desarrollador Junior',
  'Soy Michael Ramiro Cáceres, estudiante interesado en la programación, el desarrollo de software y las nuevas tecnologías. Me considero una persona autodidacta, curiosa y con iniciativa para aprender y desarrollar nuevos proyectos.\n\nTengo conocimientos en Python, desarrollo web y bases de datos, y he trabajado en proyectos utilizando tecnologías como Flask y Django. También tengo interés en el diseño, los negocios digitales y los emprendimientos, áreas en las que busco seguir creciendo y adquiriendo experiencia.\n\nMi objetivo es continuar desarrollando mis habilidades tecnológicas, participar en nuevos proyectos y construir soluciones digitales que combinen creatividad, funcionalidad e innovación.',
  'michaelramirocaceres@gmail.com',
  'https://github.com/CMRamiro',
  NULL,
  'cv.pdf'
);

-- Tecnologías (MySQL queda marcado como "aprendiendo")
INSERT INTO tecnologias (nombre, icono, aprendiendo, perfil_id) VALUES
('Python', 'fa-brands fa-python', FALSE, 1),
('HTML', 'fa-brands fa-html5', FALSE, 1),
('CSS', 'fa-brands fa-css3-alt', FALSE, 1),
('JavaScript', 'fa-brands fa-js', FALSE, 1),
('Flask', 'fa-solid fa-flask', FALSE, 1),
('Django', 'fa-solid fa-code', FALSE, 1),
('Git', 'fa-brands fa-git-alt', FALSE, 1),
('GitHub', 'fa-brands fa-github', FALSE, 1),
('Flet', 'fa-solid fa-mobile-screen', FALSE, 1),
('MySQL', 'fa-solid fa-database', TRUE, 1);

-- Formación académica
INSERT INTO formacion_academica (institucion, carrera, ubicacion, anio_inicio, anio_fin_estimado, perfil_id)
VALUES ('Instituto Técnico Renault', 'Técnico en Programación', 'Córdoba, Argentina', 2021, 2027, 1);

-- Nota: los proyectos se cargan desde el panel de administración
-- para no inventar información.
