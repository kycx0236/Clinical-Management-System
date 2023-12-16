// Selectors
// const searchInput = document.querySelector('.doccare-input-group input');
const tableRows = document.querySelectorAll('tbody tr');
const tableHeadings = document.querySelectorAll('thead th');
const deleteModal = document.getElementById('deleteModal');
const cancelModal = document.getElementById('cancelModal');
const editModal = document.getElementById('editModal');

// Event listeners
// searchInput.addEventListener('input', searchTable);
tableHeadings.forEach((head, i) => head.addEventListener('click', () => handleSortClick(i)));

function performSearch() {
    var searchTerm = $("#search-input").val();
    var filterBy = $("#filter-select").val();

    // Get the CSRF token from the meta tag
    var csrfToken = $('meta[name="csrf-token"]').attr('content');

    $.ajax({
        type: 'POST',
        url: '/receptionist/search-schedules/',
        contentType: 'application/json;charset=UTF-8',
        data: JSON.stringify({
            searchTerm: searchTerm,
            filterBy: filterBy
        }),
        headers: {
            "X-CSRFToken": csrfToken
        },
        success: function (data) {
            // Check if the data array is empty
            if (data && data.data && data.data.length > 0) {
                // Update your table with the new data
                showAlert('Data has been found.');
                updateTable(data);
            } else {
                showAlert('No data has been found.');
            }
        },
        error: function (error) {
            console.error('Error:', error.responseText);
            showAlert('An error occurred while searching for data.');
        }
    });
}


function showAlert(message) {
  // You can customize this alert to use a modal or any other UI element
  alert(message);
}

function updateTable(response) {
    // Check if the response is successful
    if (response.success) {
      var data = response.data;
  
      var tbody = document.querySelector('.doccare-table-appointment-content tbody');
      tbody.innerHTML = ''; // Clear existing rows
  
      data.forEach(function (row) {
        // Create a new row
        var newRow = document.createElement('tr');
  
        // Create cells and content for each column
        var referenceNumberCell = createTableCell('td', 'doccare-reference-number', row.scheduleID);
  
        var dateAppointmentCell = createTableCell('td', '', new Date(row.date_appointment).toLocaleDateString('en-US', { timeZone: 'Asia/Manila' }));
  
        var timeAppointmentCell = createTableCell('td', '', row.time_appointment);
  
        var slotsCell = createTableCell('td', '', row.slots);
  
        var doctorNameCell = createTableCell('td', '', row.doctorName);
  
        var actionCell = createTableCell('td', 'table__cell');
  
        // Add your action buttons/icons here
        var viewButton = createActionButton('a', 'doccare-view-appointment-icon', '/doctor/view-appointment/?reference_number=' + row.scheduleID, 'info');
  
        var editButton = createActionButton('button', 'edit-appointment-button', '', 'edit');
        editButton.setAttribute('data-id', row.scheduleID);
        editButton.setAttribute('data-date', row.date_appointment);
        editButton.setAttribute('data-time', row.time_appointment);
        editButton.setAttribute('data-slots', row.slots);
        editButton.setAttribute('data-doctorName', row.doctorName);
        editButton.onclick = function () { openEditModal(row.scheduleID, row.doctorName); };
  
        var deleteButton = createActionButton('button', 'delete-appointment-button', '', 'delete');
        deleteButton.setAttribute('data-id', row.scheduleID);
        deleteButton.setAttribute('data-doctorName', row.doctorName);
        deleteButton.onclick = function () { openDeleteModal(row.scheduleID, row.doctorName); };
  
        // Append buttons to actionCell
        actionCell.appendChild(viewButton);
        actionCell.appendChild(editButton);
        actionCell.appendChild(deleteButton);
  
        // Append cells to the row
        newRow.appendChild(referenceNumberCell);
        newRow.appendChild(dateAppointmentCell);
        newRow.appendChild(timeAppointmentCell);
        newRow.appendChild(slotsCell);
        newRow.appendChild(doctorNameCell);
        newRow.appendChild(actionCell);
  
        // Append the row to the tbody
        tbody.appendChild(newRow);
      });
    } else {
      console.error('Error in response:', response);
    }
  }
  
// Helper function to create a table cell with a specified class and content
function createTableCell(elementType, className, content) {
    var cell = document.createElement(elementType);
    if (className) {
      cell.className = className;
    }
    cell.textContent = content;
    return cell;
}
  
// Helper function to create an action button with a specified class, href (for anchor), and icon
function createActionButton(elementType, className, href, icon) {
    var button = document.createElement(elementType);
    button.className = className;
    if (elementType === 'a') {
      button.href = href;
    } else {
      button.type = 'button';
    }
    var span = document.createElement('span');
    span.className = 'material-symbols-outlined';
    span.textContent = icon;
    button.appendChild(span);
    return button;
}
  

// Sorting functionality
function handleSortClick(column) {
  tableHeadings.forEach(head => head.classList.remove('active', 'asc'));
  tableRows.forEach(row => row.querySelectorAll('td')[column].classList.remove('active'));

  tableHeadings[column].classList.add('active', 'asc');
  tableRows.forEach(row => row.querySelectorAll('td')[column].classList.add('active'));

  sortTable(column, !tableHeadings[column].classList.contains('asc'));
}

function sortTable(column, sortAsc) {
  [...tableRows].sort((a, b) => {
    const firstRow = a.querySelectorAll('td')[column].textContent.toLowerCase();
    const secondRow = b.querySelectorAll('td')[column].textContent.toLowerCase();

    return sortAsc ? (firstRow < secondRow ? 1 : -1) : (firstRow < secondRow ? -1 : 1);
  }).forEach(sortedRow => document.querySelector('tbody').appendChild(sortedRow));
}

const deleteIcons = document.querySelectorAll('.delete-appointment-button');
const editIcons = document.querySelectorAll('.edit-appointment-button');

deleteIcons.forEach(deleteIcon => {
  deleteIcon.addEventListener('click', function(event) {
    // Prevent the default action of the delete icon
    event.preventDefault();

    // Get the appointment ID and doctorName from data attributes
    const scheduleID = this.getAttribute('data-id');
    const doctorName = this.getAttribute('data-doctorName');
    console.log(scheduleID, doctorName);

    // Open the delete modal with the correct data
    openDeleteModal(scheduleID, doctorName);
  });
});

function openDeleteModal(scheduleID, doctorName) {
  // Set data attributes for appointment ID and doctorName
  deleteModal.setAttribute('data-schedule-id', scheduleID);
  deleteModal.setAttribute('data-doctor-name', doctorName);

  // Display the delete modal
  deleteModal.style.display = 'flex';
  setTimeout(() => {
    deleteModal.style.opacity = '1';
  }, 10);
  toggleOverlayBackground(true);
}

function closeDeleteModal() {
  deleteModal.style.opacity = '0';
  setTimeout(() => {
    deleteModal.style.display = 'none';
  }, 300); // Adjust the delay to match the transition duration
  toggleOverlayBackground(false);
}

// Function to toggle the overlay background
function toggleOverlayBackground(show) {
  const overlayBackgroundContainer = document.querySelector('.overlay-background-container');
  overlayBackgroundContainer.style.display = show ? 'flex' : 'none';
}

function deleteAppointment() {
  // Assuming deleteModal is your modal element
  const scheduleID = deleteModal.getAttribute('data-schedule-id');
  const csrfToken = document.querySelector('meta[name="csrf-token"]').content;
  // Make an AJAX request to delete the appointment
  $.ajax({
      type: 'POST',
      url: '/receptionist/delete-schedule/',
      data: { scheduleID: scheduleID, doctor_name: deleteModal.getAttribute('data-doctor-name') },
      headers: {
        "X-CSRFToken": csrfToken,// Include the CSRF token in the headers
      },
      success: function(response) {
          // Check the response from the server
          if (response.success) {
              const appointmentRow = document.getElementById('row-' + scheduleID);
              if (appointmentRow) {
                  appointmentRow.remove();
              }

              // Display a success message or handle as needed
              alert('Schedule deleted successfully!');
              window.location.reload(); // Refresh the page after a successful delete
          } else {
              // Display an error message or handle as needed
              alert('Failed to delete schedule.');
          }
          
          // Close the delete modal
          closeDeleteModal();
      },
      error: function() {
          // Display an error message or handle as needed
          alert('Error occurred while processing the request.');
          
          // Close the delete modal
          closeDeleteModal();
      }
  });
}

// Close the delete modal if the user clicks outside of it
window.addEventListener('click', event => {
  if (event.target === deleteModal) {
    closeDeleteModal();
  }
});

// Add a click event listener to each edit icon
editIcons.forEach(editIcon => {
  editIcon.addEventListener('click', function(event) {
    // Prevent the default action of the delete icon
    event.preventDefault();

    // Get the appointment ID from the data-id attribute
    const scheduleID = this.getAttribute('data-id');
    const doctorName = this.getAttribute('data-doctorName');
    console.log(scheduleID, doctorName);

    // Open the delete modal
    openEditModal(scheduleID);
  });
});

// Edit functionality
function openEditModal(scheduleID) {
  // Fetch appointment data asynchronously
  fetchAppointmentData(scheduleID);
}

async function fetchAppointmentData(scheduleID) {
  try {
      console.log('Scheduled ID in the async function: ', scheduleID);  
      // Make an AJAX request to fetch appointment data and time options
      const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');  // Get CSRF token from meta tag
      const response = await $.ajax({
          url: '/receptionist/get-schedule-data/',
          method: 'GET',
          data: { scheduleID: scheduleID },
          headers: {
              'X-CSRFToken': csrfToken,  // Include CSRF token in headers
          },
      });

      if (response.success) {
          // Assuming the server responds with the appointment data and time options
          const scheduleData = response.scheduleData;
          const timeOptions = response.timeOptions;
          console.log('Scheduled data in fetch', scheduleData);
          if (scheduleData) {
              // Call openEditModal with the fetched data and time options
              populateEditModal(scheduleData, timeOptions);
          } else {
              console.error('Error: Appointment data is missing in the response.');
          }
      } else {
          console.error('Error: Server response indicates failure.');
      }
  } catch (error) {
      console.error('Error fetching appointment data:', error);
      // Handle error, show a message, etc.
  }
}

// Function to populate the edit modal with data
function populateEditModal(scheduleData, timeOptions) {
  // Format the date received from the server into "yyyy-MM-dd"
  const formattedDate = new Date(scheduleData.date_appointment).toISOString().split('T')[0];
  const doctorName = document.querySelector('.edit-appointment-button').getAttribute('data-doctorName');

  // Populate the time select options
  const timeSelect = document.getElementById("validationCustom03");
  timeSelect.innerHTML = '<option value="" selected>Select your desired time</option>';

  // Check if timeOptions is defined and is an array
  if (Array.isArray(timeOptions)) {
    // Populate options based on timeOptions array
    timeOptions.forEach((timeOption) => {
      const option = document.createElement("option");
      option.value = timeOption;
      option.text = timeOption;

      // Set selected attribute if the time matches the scheduleData
      if (scheduleData.time_appointment === timeOption) {
        option.selected = true;
      }

      timeSelect.add(option);
    });
  } else {
    console.error('Error: timeOptions is not an array or is undefined.');
  }
  console.log('Populate data:', scheduleData.scheduleID);
  console.log('Populate schedule:', formattedDate);
  console.log('Populate schedule:', scheduleData.time_appointment);
  console.log('Populate schedule:', scheduleData.slots);
  console.log('Populate schedule:', scheduleData.doctorName);
  
  // Populate other form fields with the appointment data
  document.getElementById("validationCustom01").value = scheduleData.scheduleID;
  document.getElementById("validationCustom02").value = formattedDate;  // Use the formatted date
  document.getElementById("validationCustom03").value = scheduleData.time_appointment;
  document.getElementById("validationCustom04").value = scheduleData.slots;
  document.getElementById("validationCustom05").value = scheduleData.doctorName;

  // Set the reference_number in the hidden input for updating
  document.getElementsByName("scheduleID")[0].value = scheduleData.scheduleID;
  // Set the doctorName in the appropriate field
  document.getElementById("validationCustom05").value = scheduleData.doctorName;

  // Open the edit modal
  editModal.style.display = 'block';
  setTimeout(() => {
    editModal.style.opacity = '1';
  }, 10);
  toggleOverlayBackground(true);
}

function closeEditModal() {
  editModal.style.opacity = '0';
  setTimeout(() => {
    editModal.style.display = 'none';
  }, 300); // Adjust the delay to match the transition duration
  toggleOverlayBackground(false);
}
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
      window.location.href = '/receptionist/schedule/';
  });
}

// Function to show the failed modal
function showFailedModal() {
  var failedModal = document.getElementById("doccare-failed-confirmation-modal");
  failedModal.style.display = "flex";
}

const arrowBackButton = document.getElementById('arrow')
arrowBackButton.addEventListener('click', function() {
  window.location.href = '/receptionist/schedule/';
});

// Event delegation for the document
$(document).on("click", ".doccare-success-button", function (event) {
  event.preventDefault();
  editAppointment();
});


function editAppointment() {
  if (validateForm()) {
      // If the form is valid, submit it
      console.log("Form is valid. Submitting...");

      // Assuming you are using jQuery for AJAX
      $.ajax({
          // Change the url to point to the desired route
          url: '/receptionist/update-schedule/',
          method: "POST",
          data: $("form").serialize() + "&doctor_name=" + $('#validationCustom07').val(),
          success: function (response) {
              if (response.success) {
                  // Show success modal
                  showSuccessModal();

                  // Delay for 2 seconds (adjust as needed)
                  setTimeout(function () {
                      // Redirect to the /appointment/ route
                      window.location.href = '/receptionist/schedule/';
                  }, 1000);
              } else {
                  // Show failed modal
                  showFailedModal();
              }
          },
          error: function () {
              // Show failed modal in case of an error
              showFailedModal();
              // Delay for 2 seconds (adjust as needed)
              setTimeout(function () {
                // Redirect to the /appointment/ route
                window.location.href = '/receptionist/schedule/';
            }, 1000);
          }
      });
  } else {
      console.log("Form is not valid.");
  }
}

// Add event listener to cancel button
const cancelModalButton = document.querySelector('.cancel-modal-button');
cancelModalButton.addEventListener('click', closeDeleteModal);

// Add event listener to back in cancellation modal
const backModalButton = document.getElementById('back-modal-button');
backModalButton.addEventListener('click', closeCancelModal);

// Add event listener to the search form
$("#search-form").submit(function (event) {
    // Prevent the default form submission behavior
    event.preventDefault();

    // Call the performSearch function
    performSearch();
});

// Add event listener to the filter select
$("#filter-select").change(function () {
    // Call the performSearch function
    performSearch();
});
