// Selectors
// const searchInput = document.querySelector('.doccare-input-group input');
const tableRows = document.querySelectorAll('tbody tr');
const tableHeadings = document.querySelectorAll('thead th');
const deleteModal = document.getElementById('deleteModal');
const cancelModal = document.getElementById('cancelModal');

// Event listeners
// searchInput.addEventListener('input', searchTable);
tableHeadings.forEach((head, i) => head.addEventListener('click', () => handleSortClick(i)));

// Apply the Styles for STATUS at the start of the template
applyStatusStyles();


function searchAppointments(event) {
  // Prevent the default form submission behavior
  event.preventDefault();

  var searchTerm = $("#search-input").val();
  var filterBy = $("#filter-select").val();

  // Get the CSRF token from the meta tag
  var csrfToken = $('meta[name="csrf-token"]').attr('content');

  $.ajax({
      type: 'POST',
      url: '/receptionist/search-appointments/',
      contentType: 'application/json;charset=UTF-8',
      data: JSON.stringify({
          searchTerm: searchTerm,
          filterBy: filterBy
      }),
      headers: {
          "X-CSRFToken": csrfToken  // Include the CSRF token in the headers
      },
      success: function (data) {
          // Check if the data array is empty
          if (data && data.data && data.data.length > 0) {
              // Update your table with the new data
              updateTable(data);

              // Apply status styles
              applyStatusStyles();
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
      var referenceNumberCell = document.createElement('td');
      referenceNumberCell.className = 'doccare-reference-number';
      referenceNumberCell.textContent = row[0];

      var dateAppointmentCell = document.createElement('td');
      dateAppointmentCell.textContent = new Date(row[1]).toLocaleDateString('en-US', { timeZone: 'Asia/Manila' });
      
      var timeAppointmentCell = document.createElement('td');
      timeAppointmentCell.textContent = row[2];

      var lastNameCell = document.createElement('td');
      lastNameCell.textContent = row[3];

      var statusCell = document.createElement('td');
      var statusDiv = document.createElement('div');
      statusDiv.className = 'status-cell';
      var statusParagraph = document.createElement('p');
      statusParagraph.className = 'status';
      var strongStatus = document.createElement('strong');
      strongStatus.textContent = row[4];
      statusParagraph.appendChild(strongStatus);
      statusDiv.appendChild(statusParagraph);
      statusCell.appendChild(statusDiv);

      var actionCell = document.createElement('td');
      actionCell.className = 'table__cell';

      // Add your action buttons/icons here
      var viewButton = document.createElement('a');
      viewButton.href = '/receptionist/view-appointment/?reference_number=' + row[0];
      viewButton.className = 'doccare-view-appoinment-icon';
      viewButton.innerHTML = '<span class="material-symbols-outlined">info</span>';

      var rescheduleButton = document.createElement('a');
      rescheduleButton.href = '/receptionist/edit-appointment/?reference_number=' + row[0];
      rescheduleButton.className = 'doccare-edit-appoinment-icon';
      rescheduleButton.innerHTML = '<span class="material-symbols-outlined">edit</span>';

      var cancelModalButton = document.createElement('button');
      cancelModalButton.type = 'button';
      cancelModalButton.className = 'cancel-appoinment-button';
      cancelModalButton.setAttribute('data-id', row[0]);
      cancelModalButton.onclick = function () { openCancelModal(row[0]); };
      cancelModalButton.innerHTML = '<span class="material-symbols-outlined cancel-icon">event_busy</span>';

      var deleteModalButton = document.createElement('button');
      deleteModalButton.type = 'button';
      deleteModalButton.className = 'delete-appoinment-button';
      deleteModalButton.setAttribute('data-id', row[0]);
      deleteModalButton.onclick = function () { openDeleteModal(row[0]); };
      deleteModalButton.innerHTML = '<span class="material-symbols-outlined delete-icon">delete</span>';

      // Append buttons to actionCell
      actionCell.appendChild(viewButton);
      actionCell.appendChild(rescheduleButton);
      actionCell.appendChild(cancelModalButton);
      actionCell.appendChild(deleteModalButton);

      // Append cells to the row
      newRow.appendChild(referenceNumberCell);
      newRow.appendChild(dateAppointmentCell);
      newRow.appendChild(timeAppointmentCell);
      newRow.appendChild(lastNameCell);
      newRow.appendChild(statusCell);
      newRow.appendChild(actionCell);

      // Append the row to the tbody
      tbody.appendChild(newRow);
    });

    applyStatusStyles();
  } else {
    console.error('Error in response:', response);
  }
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

// Select the delete icon by its class or another appropriate selector
const deleteIcons = document.querySelectorAll('.delete-appoinment-button');
const cancelIcons = document.querySelectorAll('.cancellation-modal-button');

// Add a click event listener to each delete icon
deleteIcons.forEach(deleteIcon => {
    deleteIcon.addEventListener('click', function(event) {
        // Prevent the default action of the delete icon
        event.preventDefault();

        // Get the appointment ID from the data-id attribute
        const appointmentId = this.getAttribute('data-id');

        // Open the delete modal
        openDeleteModal(appointmentId);
    });
});

// Add a click event listener to each delete icon
cancelIcons.forEach(cancelIcon => {
  cancelIcon.addEventListener('click', function(event) {
      // Prevent the default action of the delete icon
      event.preventDefault();

      // Get the appointment ID from the data-id attribute
      const appointmentId = this.getAttribute('data-id');

      // Open the delete modal
      openCancelModal(appointmentId);
  });
});

// Delete functionality
function openDeleteModal(appointmentId) {
  deleteModal.setAttribute('data-appointment-id', appointmentId);
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
  const appointmentId = deleteModal.getAttribute('data-appointment-id');
  const csrfToken = document.querySelector('meta[name="csrf-token"]').content;
  // Make an AJAX request to delete the appointment
  $.ajax({
      type: 'POST',
      url: '/receptionist/delete-appointment/',
      data: { reference_number: appointmentId },
      headers: {
        "X-CSRFToken": csrfToken,// Include the CSRF token in the headers
      },
      success: function(response) {
          // Check the response from the server
          if (response.success) {
              const appointmentRow = document.getElementById('row-' + appointmentId);
              if (appointmentRow) {
                  appointmentRow.remove();
              }

              // Display a success message or handle as needed
              alert('Appointment deleted successfully!');
              window.location.reload(); // Refresh the page after a successful delete
          } else {
              // Display an error message or handle as needed
              alert('Failed to delete appointment.');
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


// Cancel functionality
function openCancelModal(appointmentId) {
  cancelModal.setAttribute('data-appointment-id', appointmentId);
  cancelModal.style.display = 'flex';
  setTimeout(() => {
      cancelModal.style.opacity = '1';
  }, 10);
  toggleOverlayBackground(true);
}

function closeCancelModal() {
  cancelModal.style.opacity = '0';
  setTimeout(() => {
    cancelModal.style.display = 'none';
  }, 300); // Adjust the delay to match the transition duration
  toggleOverlayBackground(false);
}

function cancelAppointment() {
  // Assuming deleteModal is your modal element
  const appointmentId = cancelModal.getAttribute('data-appointment-id');
  const csrfToken = document.querySelector('meta[name="csrf-token"]').content;
  // Make an AJAX request to delete the appointment
  $.ajax({
      type: 'POST',
      url: '/receptionist/cancel-appointment/',
      data: { reference_number: appointmentId },
      headers: {
        "X-CSRFToken": csrfToken,// Include the CSRF token in the headers
      },
      success: function(response) {
        // Check the response from the server
        if (response.success) {
            const appointmentRow = document.getElementById('row-' + appointmentId);
    
            if (appointmentRow) {
                // Disable the edit icon in the current row
                const editIcon = appointmentRow.querySelector('.doccare-edit-appoinment-icon');
                if (editIcon) {
                    editIcon.classList.add('disabled');
                    editIcon.removeAttribute('href'); // Remove the link functionality
                    console.log('appointmentId:', appointmentId);
                    console.log('appointmentRow:', appointmentRow);
                    // Optionally, you can also change the icon color or add a tooltip to indicate it's disabled
                }
            }
            console.log('appointmentId:', appointmentId);
            console.log('appointmentRow:', appointmentRow);
            // Display a success message or handle as needed
            alert('Appointment cancelled successfully!');
            window.location.reload(); // Refresh the page after a successful cancel
        } else {
            // Display an error message or handle as needed
            alert('Failed to cancel appointment.');
        }
    
        // Close the cancel modal
        closeCancelModal();
      },    
      
      error: function() {
          // Display an error message or handle as needed
          alert('Error occurred while processing the request.');
          
          // Close the delete modal
          closeDeleteModal();
      }
  });
}

// Close the cancel modal if the user clicks outside of it
window.addEventListener('click', event => {
  if (event.target === cancelModal) {
    closeCancelModal();
  }
});




// Add event listener to cancel button
const cancelModalButton = document.querySelector('.cancel-modal-button');
cancelModalButton.addEventListener('click', closeDeleteModal);

// Add event listener to back in cancellation modal
const backModalButton = document.getElementById('back-modal-button');
backModalButton.addEventListener('click', closeCancelModal);


function applyStatusStyles() {
  const statusCells = document.querySelectorAll('.status-cell');

  statusCells.forEach(cell => {
      const statusText = cell.textContent.trim().toLowerCase();

      switch (statusText) {
          case 'pending':
              cell.style.backgroundColor = '#fbedd0';
              cell.style.color = '#b17806';
              cell.style.paddingLeft = '15px'; // Adjust the value as needed
              break;
          case 'cancelled':
              cell.style.backgroundColor = '#FFCCCB';
              cell.style.color = '#F00';
              cell.style.paddingLeft = '15px'; // Adjust the value as needed
              break;
          case 'done':
              cell.style.backgroundColor = '#86E49D';
              cell.style.color = '#006b21';
              cell.style.paddingLeft = '15px'; // Adjust the value as needed
              break;
          case 'scheduled':
              cell.style.backgroundColor = '#DFF1FF';
              cell.style.color = '#0277BD';
              cell.style.paddingLeft = '15px'; // Adjust the value as needed
              break;
          case 'rescheduled':
              cell.style.backgroundColor = '#FFC';
              cell.style.color = '#7A760A';
              cell.style.paddingLeft = '15px'; // Adjust the value as needed
              break;
          // Add more cases as needed
          default:
              // Default styles if status doesn't match any case
              cell.style.backgroundColor = 'initial';
              cell.style.color = 'initial';
              cell.style.paddingLeft = 'initial';
      }
  });
}

// Add event listener to the search form
$("#search-form").submit(searchAppointments);
// Add event listener to the filter select
$("#filter-select").change(searchAppointments);