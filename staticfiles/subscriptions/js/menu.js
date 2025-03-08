document.addEventListener("DOMContentLoaded", function () {
    console.log("JavaScript Loaded Successfully! ✅");

    // ✅ Fix Menu Toggle
    const menuIcon = document.getElementById("menu-icon");
    const menuLinks = document.getElementById("h");  // Correct reference

    if (menuIcon && menuLinks) {
        menuIcon.addEventListener("click", function() {
            menuLinks.classList.toggle("active");
        });

        window.addEventListener("resize", function() {
            if (window.innerWidth > 768) {
                menuLinks.classList.remove("active");
            }
        });
    }
});