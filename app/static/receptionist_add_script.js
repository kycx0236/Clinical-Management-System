const continueButton = document.getElementById('add-continue-button');
const form = document.querySelector('.needs-validation');
const firstNameInput = document.getElementById('validationCustom01');
const middleNameInput = document.getElementById('validationCustom02');
const lastNameInput = document.getElementById('validationCustom03');
const dateOfBirthInput = document.getElementById('validationCustom04');
const sexInput = document.getElementById('validationCustom05');
const addressInput = document.getElementById('validationCustom06');
const contactNumberInput = document.getElementById('validationCustom07');
const backButton = document.getElementById('add-appoinment-back-button');
const submitButton = document.getElementById('add-appoinment-submit-button');
const dateAppointmentInput = document.getElementById('validationCustom08');
const timeAppointmentInput = document.getElementById('validationCustom09');
const emailInput = document.getElementById('validationCustom10');
const csrfTokenInput = document.querySelector('input[name="csrf_token"]').value;

// Function to handle form transition and validation
function handleFormTransition() {
    // Check individual field validity
    const isFirstNameValid = firstNameInput.checkValidity();
    const isMiddleNameValid = middleNameInput.checkValidity();
    const isLastNameValid = lastNameInput.checkValidity();
    const isDateOfBirthValid = dateOfBirthInput.checkValidity();
    const isSexValid = sexInput.checkValidity();
    const isAddressValid = addressInput.checkValidity();
    const isContactNumberValid = contactNumberInput.checkValidity();

    // Check if all individual fields are valid
    if (isFirstNameValid && isMiddleNameValid && isLastNameValid && isDateOfBirthValid && isSexValid && isAddressValid && isContactNumberValid) {
        // Transition to the next page
        console.log('All fields are valid');
        const firstForms = document.getElementById('appointment-first-forms');
        const secondForms = document.getElementById('appointment-second-forms');
        const numberOne = document.getElementById('number-one');
        const numberTwo = document.getElementById('number-two');
        const paragraph = document.getElementById('doccare-add-appointment-paragraph');

        // Toggle visibility of forms
        firstForms.style.display = 'none';
        secondForms.style.display = 'block';
        paragraph.style.display = 'none';

        // Animate the transition of numbers
        numberOne.style.transition = 'transform 0.5s ease';
        numberOne.style.transform = 'scale(1.00)';
        numberOne.style.background = 'rgba(2, 119, 189, 0.50)';

        numberTwo.style.transition = 'transform 0.5s ease';
        numberTwo.style.transform = 'scale(1.25)';
        numberTwo.style.background = '#0277BD';

        // Ensure the second form becomes visible
        secondForms.style.display = 'block';
    } else {
        // If any field is invalid, prevent form submission and display validation styles
        console.log('Some fields contain validation errors');
        form.classList.add('was-validated');
    }
}

// Add an event listener to the CONTINUE button
continueButton.addEventListener('click', handleFormTransition);

// Function to go back to the previous form
function handleFormBackTransition() {
    const firstForms = document.getElementById('appointment-first-forms');
    const secondForms = document.getElementById('appointment-second-forms');
    const numberOne = document.getElementById('number-one');
    const numberTwo = document.getElementById('number-two');

    // Toggle visibility of forms
    firstForms.style.display = 'block';
    secondForms.style.display = 'none';
    
    // Animate the transition of number-two
    numberOne.style.transition = 'transform 0.5s ease';
    numberOne.style.transform = 'scale(1.25)';
    numberOne.style.background = '#0277BD';
    
    numberTwo.style.transition = 'transform 0.5s ease';
    numberTwo.style.transform = 'scale(1.00)';
    numberTwo.style.background = 'rgba(2, 119, 189, 0.50)'; 
}

// Add an event listener to the BACK button
backButton.addEventListener('click', handleFormBackTransition);


// Add the function to handle the form submission
function handleFormSubmission() {
    // Check individual field validity
    const isDateAppointmentValid = dateAppointmentInput.checkValidity();
    const isTimeAppointmentValid = timeAppointmentInput.checkValidity();
    const isEmailValid = emailInput.checkValidity();

    // Check if all individual fields are valid
    if (isDateAppointmentValid && isTimeAppointmentValid && isEmailValid) {
        // Create a FormData object to handle the form data
        const formData = new FormData();

        // Append each form field to the FormData object
        formData.append('first_name', firstNameInput.value);
        formData.append('middle_name', middleNameInput.value);
        formData.append('last_name', lastNameInput.value);
        formData.append('birth_date', dateOfBirthInput.value);
        formData.append('sex', sexInput.value);
        formData.append('address', addressInput.value);
        formData.append('contact_number', contactNumberInput.value);
        formData.append('date_appointment', dateAppointmentInput.value);
        formData.append('time_appointment', timeAppointmentInput.value);
        formData.append('email', emailInput.value);
        formData.append('csrf_token', formData.get('csrf_token'));  // Include CSRF token

        // Perform AJAX request to submit form data
        fetch('/receptionist/add-appointment/', {
            method: 'POST',
            body: formData,  // Use FormData instead of JSON.stringify
            headers: {
                'X-CSRFToken': formData.get('csrf_token')  // Include CSRF token in headers
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                console.log('Server response:', data);
                // Successful submission, redirect to success modal or do something else
                console.log('Form submitted successfully');
                // Redirect to success modal or perform any other action
            } else {
                // Handle submission failure
                console.error('Form submission failed:', data.message);
                // Display an error message or handle the failure appropriately
            }
        })
        .catch(error => {
            console.error('Error during form submission:', error);
            // Handle the error appropriately
        });
    } else {
        // If any field is invalid, prevent form submission and display validation styles
        console.log('Some fields contain validation errors');
        form.classList.add('was-validated');
    }
}
// Add an event listener to the SUBMIT button
submitButton.addEventListener('click', handleFormSubmission);