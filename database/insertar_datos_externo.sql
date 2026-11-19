INSERT INTO perfil (
    usuario_id, nombre_completo, titulo, presentacion, sobre_mi, objetivo,
    email, github_url, ubicacion, foto, cv_archivo
)
SELECT
    id,
    'Michael Ramiro Cáceres',
    'Desarrollador Junior',
    'Estudiante de Técnico en Programación interesado en el desarrollo de software y las nuevas tecnologías.',
    'Soy Michael Ramiro Cáceres, estudiante interesado en la programación, el desarrollo de software y las nuevas tecnologías. Me considero una persona autodidacta, curiosa y con iniciativa para aprender y desarrollar nuevos proyectos.',
    'Continuar desarrollando mis habilidades tecnológicas, participar en nuevos proyectos y construir soluciones digitales que combinen creatividad, funcionalidad e innovación.',
    'michaelramirocaceres@gmail.com',
    'https://github.com/CMRamiro',
    'Córdoba, Argentina',
    'cmrfoto.png',
    'cv.pdf'
FROM usuarios
WHERE es_admin = TRUE
ORDER BY id
LIMIT 1;

INSERT INTO tecnologias (nombre, icono, estado, orden) VALUES
('Python', 'fa-brands fa-python', 'Intermedio', 1),
('HTML', 'fa-brands fa-html5', 'Avanzado', 2),
('CSS', 'fa-brands fa-css3-alt', 'Intermedio', 3),
('JavaScript', 'fa-brands fa-js', 'Intermedio', 4),
('Flask', 'fa-solid fa-flask', 'Intermedio', 5),
('Django', 'fa-solid fa-code', 'Conocimiento', 6),
('Git', 'fa-brands fa-git-alt', 'Intermedio', 7),
('GitHub', 'fa-brands fa-github', 'Intermedio', 8),
('Flet', 'fa-solid fa-mobile-screen', 'Conocimiento', 9),
('MySQL', 'fa-solid fa-database', 'Aprendiendo', 10);

INSERT INTO formacion_academica (
    institucion, titulo, descripcion, fecha_inicio, fecha_fin, en_curso, orden
)
VALUES (
    'Instituto Técnico Renault',
    'Técnico en Programación',
    'Formación técnica en programación y desarrollo de software.',
    '2021',
    '2027',
    TRUE,
    1
);
