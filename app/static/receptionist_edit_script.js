document.addEventListener("DOMContentLoaded", function () {
    // Validate the form on submit
    $(".doccare-success-button").on("click", function (event) {
        event.preventDefault();
        if (validateForm()) {
            // If the form is valid, submit it
            console.log("Form is valid. Submitting...");

            // Assuming you are using jQuery for AJAX
            $.ajax({
                url: document.querySelector("form").action,
                method: "POST",
                data: $("form").serialize(),
                success: function (response) {
                    if (response.success) {
                        // Show success modal
                        showSuccessModal();
                
                        // Delay for 2 seconds (adjust as needed)
                        setTimeout(function () {
                            // Redirect to the /appointment/ route
                            window.location.href = '/receptionist/appointment/';
                        }, 1000);
                    } else {
                        // Show failed modal
                        showFailedModal();
                    }
                },
                error: function () {
                    // Show failed modal in case of an error
                    showFailedModal();
                }
            });
        } else {
            console.log("Form is not valid.");
        }
    });

    // Function to validate the form
    function validateForm() {
        var form = document.querySelector(".needs-validation");
        var isValid = form.checkValidity();

        // Check each form field for validity
        form.querySelectorAll(".form-control").forEach(function (input) {
            input.reportValidity();
        });

        return isValid;
    }

    // Function to show the success modal
    function showSuccessModal() {
        var successModal = document.getElementById("doccare-success-confirmation-modal");
        successModal.style.display = "flex";

        // Add event listener to the "Done" button inside the success modal
        // Assuming you have an element with id "doccare-done-modal-button" for the "Done" button
        var doneButton = document.getElementById("doccare-done-modal-button");

        doneButton.addEventListener('click', async function() {
            // Show the success modal
            $("#doccare-success-confirmation-modal").modal("show");

            // Use a Promise to wait for the modal to be fully displayed
            await new Promise(resolve => {
                $('#doccare-success-confirmation-modal').on('shown.bs.modal', function () {
                    // Resolve the Promise when the modal is fully displayed
                    resolve();
                });
            });

            // Redirect to the /appointment/ route
            window.location.href = '/receptionist/appointment/';
        });
    }

    // Function to show the failed modal
    function showFailedModal() {
        var failedModal = document.getElementById("doccare-failed-confirmation-modal");
        failedModal.style.display = "flex";
    }
    const arrowBackButton = document.getElementById('arrow')
    arrowBackButton.addEventListener('click', function() {
        // Redirect to the /appointment/ route
        window.location.href = '/receptionist/appointment/';
    });
});
