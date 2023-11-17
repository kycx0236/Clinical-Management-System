const continueButton = document.getElementById('add-continue-button');
const form = document.querySelector('.needs-validation');
const firstNameInput = document.getElementById('validationCustom01');
const middleNameInput = document.getElementById('validationCustom02');
const lastNameInput = document.getElementById('validationCustom03');
const dateofBirthInput = document.getElementById('validationCustom04');
const sexInput = document.getElementById('validationCustom05');
const addressInput = document.getElementById('validationCustom06');
const contactNumberInput = document.getElementById('validationCustom07');
const backButton = document.getElementById('add-appoinment-back-button');

// Function to handle form transition and validation
function handleFormTransition() {
    // Check individual field validity
    const isFirstNameValid = firstNameInput.checkValidity();
    const isMiddleNameValid = middleNameInput.checkValidity();
    const isLastNameValid = lastNameInput.checkValidity();
    const isDateOfBirthValid = dateofBirthInput.checkValidity();
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