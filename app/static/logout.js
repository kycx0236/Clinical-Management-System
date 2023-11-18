window.onload = function() {
    // Display the confirmation modal
    document.getElementById("logoutButton").addEventListener("click", function() {
        document.getElementById("logoutModal").style.display = "flex";
    });

    // Close the confirmation modal on cancel
    document.getElementById("cancelLogout").addEventListener("click", function() {
        document.getElementById("logoutModal").style.display = "none";
    });

    // Handle the confirm logout
    document.getElementById("confirmLogout").addEventListener("click", function() {
        // You can add your logic here to perform the logout action
        console.log("Performing logout action");

        // Close the confirmation modal after logout
        document.getElementById("logoutModal").style.display = "none";

        // Redirect to the logout URL
        window.location.href = logoutUrl;
    });
};