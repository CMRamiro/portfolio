// JavaScript sencillo para el portfolio
// Funcionalidad: abrir/cerrar el menú en pantallas pequeñas (responsive)

document.addEventListener("DOMContentLoaded", function () {
    const menuToggle = document.getElementById("menu-toggle");
    const navLinks = document.getElementById("nav-links");

    if (menuToggle && navLinks) {
        menuToggle.addEventListener("click", function () {
            navLinks.classList.toggle("active");
        });

        // Cerrar el menú al hacer clic en un enlace
        const links = navLinks.querySelectorAll("a");
        links.forEach(function (link) {
            link.addEventListener("click", function () {
                navLinks.classList.remove("active");
            });
        });
    }
});
