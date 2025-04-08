document.getElementById("flower-container").addEventListener("click", function () {
    console.log("flower-container is blocking clicks!");
});

document.addEventListener("DOMContentLoaded", function () {
    console.log("JavaScript Loaded Successfully! ");

    // Menu toggle
    const menuIcon = document.getElementById("menu-icon");
    const menuLinks = document.getElementById("h");  

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

    // Rectangle Hover Animation
    const columns = document.querySelectorAll('.f_col');

columns.forEach(column => {
    const rectangles = column.querySelectorAll('.rectangle');

    rectangles.forEach(rectangle => {
        let animationFrameId;

        column.addEventListener('mousemove', (e) => {
            let rect = column.getBoundingClientRect();
            let x = (e.clientX - rect.left) / rect.width - 0.5;
            let y = (e.clientY - rect.top) / rect.height - 0.5;

            // Increase rotation angles for more shake
            let rotateY = x * 30; // More intense shake (was 20)
            let rotateX = y * -30;

            // Smooth animation using requestAnimationFrame
            cancelAnimationFrame(animationFrameId);
            animationFrameId = requestAnimationFrame(() => {
                rectangle.style.transform = `rotateY(${rotateY}deg) rotateX(${rotateX}deg) scale(1.05)`;
            });
        });

        column.addEventListener('mouseleave', () => {
            cancelAnimationFrame(animationFrameId);
            rectangle.style.transition = "transform 0.5s ease-out"; // Smooth return
            rectangle.style.transform = "rotateY(0deg) rotateX(0deg) scale(1)";
        });
    });
});



    //  Take Test Button (Modal)
    const modal = document.getElementById("testSelectionModal");
    const closeModal = document.querySelector(".close");

    if (!modal || !closeModal) {
        console.error("Modal elements are missing!");
        return;
    }else{

    document.querySelectorAll(".takeTestBtn").forEach(btn => {
        btn.addEventListener("click", function(event) {
            event.preventDefault();
            modal.style.display = "flex";  // Force visibility
        });
    });}

    closeModal.addEventListener("click", function () {
        console.log("Close Modal Button Clicked!");
        modal.style.display = "none";
    });

    window.addEventListener("click", function (event) {
        if (event.target == modal) {
            console.log("Modal Background Clicked!");
            modal.style.display = "none";
        }
    });



    //upload docs
    const sendDocsButton = document.querySelector(".rectangles_send_docs .visit_site");

    if (sendDocsButton) {
        sendDocsButton.addEventListener("click", function (event) {
            event.preventDefault(); // Prevent default link behavior
            window.location.href = "{% url 'upload_document' %}"; // Redirect to upload_document.html
        });
    }
});
