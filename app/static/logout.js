window.onload = function() {
    document.getElementById("logoutButton").addEventListener("click", function() {
        document.getElementById("logoutModal").style.display = "block";
    });

    document.getElementById("cancelLogout").addEventListener("click", function() {
        document.getElementById("logoutModal").style.display = "none";
    });

    document.getElementById("confirmLogout").addEventListener("click", function() {
        console.log("Performing logout action");

        document.getElementById("logoutModal").style.display = "none";

        window.location.href = logoutUrl;
    });
};