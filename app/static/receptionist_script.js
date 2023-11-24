// Selectors
const searchInput = document.querySelector('.doccare-input-group input');
const tableRows = document.querySelectorAll('tbody tr');
const tableHeadings = document.querySelectorAll('thead th');
const deleteModal = document.getElementById('deleteModal');

// Event listeners
searchInput.addEventListener('input', searchTable);
tableHeadings.forEach((head, i) => head.addEventListener('click', () => handleSortClick(i)));

// Apply the Styles for STATUS at the start of the template
applyStatusStyles();


// Search functionality
function searchTable() {
  const searchValue = searchInput.value.toLowerCase();

  tableRows.forEach((row, i) => {
    const rowData = row.textContent.toLowerCase();
    const isMatch = rowData.includes(searchValue);

    row.classList.toggle('hide', !isMatch);
    row.style.setProperty('--delay', i / 25 + 's');

    // Reset background color for even rows
    row.style.backgroundColor = i % 2 === 0 ? '#ecf6ff' : '';
  });

  const visibleRows = document.querySelectorAll('tbody tr:not(.hide)');
  visibleRows.forEach((visibleRow, i) => {
    visibleRow.style.backgroundColor = i % 2 === 0 ? '#fff5' : '#ecf6ff';
  });
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

// Delete functionality
function openDeleteModal(appointmentId) {
  deleteModal.setAttribute('data-appointment-id', appointmentId);
  deleteModal.style.display = 'flex';
  toggleOverlayBackground(true);
}

function closeDeleteModal() {
  deleteModal.style.display = 'none';
  toggleOverlayBackground(false); // Close the overlay background when closing the modal
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

// Add event listener to cancel button
const cancelModalButton = document.querySelector('.cancel-modal-button');
cancelModalButton.addEventListener('click', closeDeleteModal);


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
              cell.style.backgroundColor = '#d893a3';
              cell.style.color = '#b30021';
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
          // Add more cases as needed
          default:
              // Default styles if status doesn't match any case
              cell.style.backgroundColor = 'initial';
              cell.style.color = 'initial';
              cell.style.paddingLeft = 'initial';
      }
  });
}
