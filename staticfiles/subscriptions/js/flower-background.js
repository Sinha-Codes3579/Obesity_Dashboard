document.addEventListener("DOMContentLoaded", () => {
    const container = document.getElementById("flower-container");

    function createFlower() {
        const flower = document.createElement("div");
        flower.classList.add("flower");

        // Random position and size
        const size = Math.random() * 30 + 20;
        flower.style.width = `${size}px`;
        flower.style.height = `${size}px`;
        flower.style.left = `${Math.random() * 100}vw`;

        // Random colors
        const colors = ["#121212", "#FFC0CB", "#FF0099", "#E0E0E0", "#B0B0B0"];
        flower.style.backgroundColor = colors[Math.floor(Math.random() * colors.length)];

        // Random animation speed
        flower.style.animationDuration = `${Math.random() * 5 + 5}s`;

        // Add to the container
        container.appendChild(flower);

        // Remove flower after animation
        setTimeout(() => {
            flower.remove();
        }, 10000);
    }

    // Create flowers continuously
    setInterval(createFlower, 500);
});
