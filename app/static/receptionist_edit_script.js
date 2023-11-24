const referenceNumberInput = document.getElementById('validationCustom01');
const dateAppointmentInput = document.getElementById('validationCustom02');
const timeAppointmentInput = document.getElementById('validationCustom03');
const statusInput = document.getElementById('validationCustom04');
const firstNameInput = document.getElementById('validationCustom05');
const middleNameInput = document.getElementById('validationCustom06');
const lastNameInput = document.getElementById('validationCustom07');
const sexInput = document.getElementById('validationCustom08');
const dateOfBirthInput = document.getElementById('validationCustom09');
const contactNumberInput = document.getElementById('validationCustom10');
const emailInput = document.getElementById('validationCustom11');
const addressInput = document.getElementById('validationCustom12');
const form = document.querySelector('.needs-validation');
const submitButton = document.getElementById('doccare-success-button');
const csrfTokenInput = document.querySelector('input[name="csrf_token"]').value;
const doneButton = document.querySelector('.doccare-done-modal-button');

// Function to handle success modal
function successModal(booking_details) {
    console.log('Inside successModal function');
    console.log(document.getElementById('doccare-success-modal'));
    const successModal = document.getElementById('doccare-success-modal');
    console.log('successModal:', successModal);

    // Check if the modal element is found
    if (successModal) {
        // Toggle the visibility of the modal
        successModal.style.display = 'flex';

        // Display booking details in the modal
        const bookingDetailsContainer = document.getElementById('doccare-success-modal-content-2');

        if (booking_details && booking_details.last_name) {
            // Format the date with Philippine timezone and full month name
            const options = { timeZone: 'Asia/Manila', weekday: 'long', day: 'numeric', month: 'long', year: 'numeric' };
            const formattedDate = new Date(booking_details.date_appointment).toLocaleDateString('en-PH', options);

            bookingDetailsContainer.innerHTML = `<p>Last Name: ${booking_details.last_name}</p>
                                                <p>Appointment Schedule: ${formattedDate} ${booking_details.time_appointment}</p>
                                                <p>Booking Reference No.: ${booking_details.reference_number}</p>`;
            console.log('Booking details fetch!');
        } else {
            failureModal();
        }
    } else {
        console.error('Could not find the modal element with ID doccare-success-modal');
        // You may want to handle this case appropriately, e.g., show an error message
    }
}

// Function to format time from "hh:mm AM/PM" to "HH:mm"
function formatTime(inputTime) {
    const timeParts = inputTime.split(' ');
    const time = timeParts[0];
    const period = timeParts[1];

    // Convert 12-hour time to 24-hour time
    const [hours, minutes] = time.split(':');
    let formattedHours = parseInt(hours, 10);

    if (period === 'PM' && formattedHours < 12) {
        formattedHours += 12;
    } else if (period === 'AM' && formattedHours === 12) {
        formattedHours = 0;
    }

    // Format the time in "HH:mm" format
    const formattedTime = `${formattedHours.toString().padStart(2, '0')}:${minutes}`;

    return formattedTime;
}   

// Add the function to handle the form submission
async function handleFormSubmission() {
    // Check individual field 
    const isReferenceNumberValid = referenceNumberInput.checkValidity();
    const isDateAppointmentValid = dateAppointmentInput.checkValidity();
    const isTimeAppointmentValid = timeAppointmentInput.checkValidity();
    const isStatusValid = statusInput.checkValidity();
    const isFirstNameValid = firstNameInput.checkValidity();
    const isMiddleNameValid = middleNameInput.checkValidity();
    const isLastNameValid = lastNameInput.checkValidity();
    const isSexValid = sexInput.checkValidity();
    const isDateOfBirthValid = dateOfBirthInput.checkValidity();
    const isContactNumberValid = contactNumberInput.checkValidity();
    const isEmailValid = emailInput.checkValidity();
    const isAddressValid = addressInput.checkValidity();

    // Define data variable to store the response data
    let data;

    // Check if all individual fields are valid
    if (isReferenceNumberValid && isDateAppointmentValid && isTimeAppointmentValid && isStatusValid && isFirstNameValid && isMiddleNameValid && isLastNameValid && isSexValid && isDateOfBirthValid && isContactNumberValid && isEmailValid && isAddressValid) {
        console.log('All fields are valid');
        // Create a FormData object to handle the form data
        const formData = new FormData();

        // Append each form field to the FormData object
        formData.append('reference_number', referenceNumberInput.value);
        formData.append('date_appointment', dateAppointmentInput.value);
        formData.append('time_appointment', timeAppointmentInput.value);
        formData.append('status_', statusInput.value);
        formData.append('first_name', firstNameInput.value);
        formData.append('middle_name', middleNameInput.value);
        formData.append('last_name', lastNameInput.value);
        formData.append('sex', sexInput.value);
        formData.append('birth_date', dateOfBirthInput.value);
        formData.append('contact_number', contactNumberInput.value);
        formData.append('email', emailInput.value);
        formData.append('address', addressInput.value);
        formData.append('csrf_token', csrfTokenInput);  // Use the csrfTokenInput directly

        try {
            // Perform AJAX request to submit form data
            const response = await fetch('/receptionist/add-appointment/', {
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
    else {
        // If any field is invalid, prevent form submission and display validation styles
        console.log('Some fields contain validation errors');
        form.classList.add('was-validated');
    }
}
// Function to handle failure modal
function failureModal() {
    console.log('Inside failureModal function');
    const failedConfirmationModal = document.getElementById('doccare-failed-confirmation-modal');

    // Toggle the visibility of the modal
    failedConfirmationModal.style.display = 'flex';

    // Display a message in the modal
    const failedModalContent = document.getElementById('doccare-failed-modal-content');
    failedModalContent.innerHTML = '<h1>Something went Wrong!</h1><p class="text-muted">Booking details are being processed. Please wait...</p>';
}

// Add an event listener to the SUBMIT button
submitButton.addEventListener('click', async function (event) {
    event.preventDefault(); // Prevent the default button click behavior
    // Handle form submission
    const response = await handleFormSubmission();

    if (response.success) {
        // Call successModal with booking details from the response
        successModal(response.booking_details);
    } else {
        // Call failureModal when submission fails
        failureModal();
    }
});

doneButton.addEventListener('click', function () {
    // Redirect to the /appointment/ route
    window.location.href = '/receptionist/appointment/';
});