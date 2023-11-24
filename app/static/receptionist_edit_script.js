document.addEventListener('DOMContentLoaded', function () {
    // Get the form and modal elements
    const editForm = document.querySelector('.needs-validation');
    const successModal = document.getElementById('doccare-success-modal');
    const failedModal = document.getElementById('doccare-failed-confirmation-modal');

    // Add an event listener to the form for submission
    editForm.addEventListener('submit', function (event) {
        event.preventDefault(); // Prevent the default form submission

        // Perform any additional validation if needed

        // Convert form data to JSON
        const formData = new FormData(editForm);
        const jsonData = {};
        formData.forEach((value, key) => {
            jsonData[key] = value;
        });

        // Include CSRF token in headers
        const csrfToken = document.querySelector('[name=csrf_token]').value;

        // Simulate form submission using Fetch API
        fetch(editForm.action, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken, // Include CSRF token in headers
            },
            body: JSON.stringify(jsonData),
        })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                // Check the success status from the response
                if (data.success) {
                    // Show the success modal
                    showSuccessModal(data.booking_details);
                } else {
                    // Show the failed modal
                    showFailedModal();
                }
            })
            .catch(error => {
                console.error('Error submitting form:', error);
                // Show the failed modal in case of an error
                showFailedModal();
            });
    });

    // Function to show the success modal
    function showSuccessModal(bookingDetails) {
        // Update the modal content with booking details
        const lastNameElement = document.getElementById('patient-lastname');
        const appointmentElement = document.getElementById('patient-appoinment');
        const referenceElement = document.getElementById('patient-reference');

        lastNameElement.textContent = 'Last Name: ' + bookingDetails.last_name;
        appointmentElement.textContent = 'Appointment Schedule: ' + bookingDetails.date_appointment + ' ' + bookingDetails.time_appointment;
        referenceElement.textContent = 'Booking Reference No.: ' + bookingDetails.reference_number;

        // Show the success modal
        successModal.style.display = 'flex';
    }

    // Function to show the failed modal
    function showFailedModal() {
        // Show the failed modal
        failedModal.style.display = 'flex';
    }

    // Close modals when the "DONE" button is clicked
    const doneButtons = document.querySelectorAll('.doccare-done-modal-button');
    doneButtons.forEach(button => {
        button.addEventListener('click', function () {
            successModal.style.display = 'none';
            failedModal.style.display = 'none';
        });
    });
});
