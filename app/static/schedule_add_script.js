const dateAppointmentInput = document.getElementById('validationCustom01');
const timeAppointmentInput = document.getElementById('validationCustom02');
const slotsInput = document.getElementById('validationCustom03');
const doctorNameInput = document.getElementById('validationCustom11');
const doctorIDInput = document.getElementById('validationCustom12');
const csrfTokenInput = document.querySelector('input[name="csrf_token"]').value;
const formInput = document.getElementById('appointment-form');
const arrowBackButton = document.getElementById('arrow');
const submitButton = document.getElementById('doccare-submit-button');
const doneButton = document.querySelector('.doccare-done-modal-button');

// Function to handle success modal
function successModal() {
    console.log('Inside successModal function');
    const successModal = document.getElementById('doccare-success-modal');

    // Toggle the visibility of the modal
    successModal.style.display = 'flex';
}

// Add the function to handle the form submission
async function handleFormSubmission() {
    // Check individual field validity
    const isDateAppointmentValid = dateAppointmentInput.checkValidity();
    console.log('Status: ' + isDateAppointmentValid);
    const isTimeAppointmentValid = timeAppointmentInput.checkValidity();
    console.log('Status: ' + isTimeAppointmentValid);
    const isSlotsValid = slotsInput.checkValidity();
    console.log('Status: ' + isSlotsValid);
    const isDoctorNameValid = doctorNameInput.checkValidity();
    console.log('Status: ' + isDoctorNameValid); 
    const isDoctorIDValid = doctorIDInput.checkValidity();
    console.log('Status: ' + isDoctorIDValid);

    // Define data variable to store the response data
    let data;

    // Check if all individual fields are valid
    if (isDateAppointmentValid && isTimeAppointmentValid && isSlotsValid && isDoctorIDValid && isDoctorNameValid) {
        // Create a FormData object to handle the form data
        const formData = new FormData();

        console.log(dateAppointmentInput); 
        console.log(timeAppointmentInput);
        console.log(formData);

        // Append each form field to the FormData object
        formData.append('date_appointment', dateAppointmentInput.value);
        formData.append('time_appointment', timeAppointmentInput.value);
        formData.append('slots', slotsInput.value);
        formData.append('doctorID', doctorIDInput.value);
        formData.append('doctorName', doctorNameInput.value)
        formData.append('csrf_token', csrfTokenInput);  // Use the csrfTokenInput directly

        try {
            // Perform AJAX request to submit form data
            const response = await fetch('/receptionist/add-schedule/', {
                method: 'POST',
                body: formData,  // Use FormData instead of JSON.stringify
                headers: {
                    'X-CSRFToken': csrfTokenInput  // Include CSRF token in headers
                }
            });
    
            // Check if the response is successful
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
    
            // Check the content type of the response
            const contentType = response.headers.get('content-type');
            if (contentType && contentType.includes('application/json')) {
                // Parse the JSON response
                data = await response.json();
                // Handle the JSON data as needed
                if (data.success) {
                    // Successful submission
                    console.log('Server response:', data);
                    console.log('Form submitted successfully');
                    // Redirect to success modal or perform any other action
                } else {
                    // Handle submission failure
                    console.error('Form submission failed:', data.message);
                    alert('Form validation failed. Please check the highlighted fields.') ;
                    // Display an error message or handle the failure appropriately
                }
            } else {
                // The response is not in JSON format
                console.error('Unexpected response content type:', contentType);
                // Handle the error appropriately, for example, show an error message
            }
        } catch (error) {
            // Handle other errors, such as network errors
            console.error('Error during form submission:', error);
        }
    
        // Return the data variable
        return data;
    }
}
// Add an event listener to the SUBMIT button
submitButton.addEventListener('click', async function() {
    // Remove the event listener to prevent multiple clicks
    submitButton.removeEventListener('click', arguments.callee);

    // Handle form submission
    const response = await handleFormSubmission();

    // Re-enable the button after the form submission is complete
    submitButton.disabled = false;

    // Call successModal with booking details from the response
    successModal(response);
    setTimeout(function () {
        // Redirect to the /appointment/ route
        window.location.href = '/receptionist/schedule/';
    }, 700);
});

doneButton.addEventListener('click', function() {
    // Redirect to the /appointment/ route
    window.location.href = '/receptionist/schedule/';
});


arrowBackButton.addEventListener('click', function() {
    // Redirect to the /appointment/ route
    window.location.href = '/receptionist/schedule/';
});