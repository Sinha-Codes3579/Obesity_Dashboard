// supscription section

document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("emailForm").addEventListener("submit", function (event) {
        event.preventDefault();  // Stop default form submission

        let formData = new FormData(this);
        fetch(this.action, {
            method: "POST",
            body: formData,
        })
        .then(response => response.json())
        .then(data => {
            let messageDiv = document.getElementById("subscription-message");
            if (data.message) {
                messageDiv.innerHTML = `<p style="color: green;">${data.message}</p>`;
            } else if (data.error) {
                messageDiv.innerHTML = `<p style="color: red;">${data.error}</p>`;
            }
        })
        .catch(error => console.error("Error:", error));
    });
});

document.addEventListener("DOMContentLoaded", function () {
    const openLoginBtn = document.getElementById("openLoginBtn");
    const openSignupBtn = document.getElementById("openSignupBtn");
    const loginPopup = document.getElementById("loginPopup");
    const signupPopup = document.getElementById("signupPopup");
    const closeLoginBtn = loginPopup.querySelector(".close-login");
    const closeSignupBtn = signupPopup.querySelector(".close-signup");

    function openPopup(popup) {
        closeAllPopups();
        popup.style.display = "flex";
        popup.style.animation = "fadeIn 0.3s ease-in-out";
    }

    function closePopup(popup) {
        popup.style.animation = "fadeOut 0.3s ease-in-out";
        setTimeout(() => {
            popup.style.display = "none";
        }, 300);
    }

    function closeAllPopups() {
        loginPopup.style.display = "none";
        signupPopup.style.display = "none";
    }

    openLoginBtn.addEventListener("click", function () {
        openPopup(loginPopup);
    });

    openSignupBtn.addEventListener("click", function () {
        openPopup(signupPopup);
    });

    closeLoginBtn.addEventListener("click", function () {
        closePopup(loginPopup);
    });

    closeSignupBtn.addEventListener("click", function () {
        closePopup(signupPopup);
    });

    // Close popup when clicking outside
    window.addEventListener("click", function (event) {
        if (event.target === loginPopup) {
            closePopup(loginPopup);
        }
        if (event.target === signupPopup) {
            closePopup(signupPopup);
        }
    });
});
