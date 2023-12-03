document.addEventListener("DOMContentLoaded", function () {
  const filterSelect = document.getElementById("filter-select");
  const rows = document.querySelectorAll(".doccare-table-appointment-content tbody tr");
  
  filterSelect.addEventListener("change", function () {
      const selectedValue = filterSelect.value.toUpperCase();

      rows.forEach(function (row) {
          const statusCell = row.querySelector(".status-cell strong");
          const status = statusCell.innerText.toUpperCase();

          if (selectedValue === "ALL" || status === selectedValue) {
              row.style.display = "";
          } else {
              row.style.display = "none";
          }
      });

  });
});
                        
                        
  $("#search-icon").click(function () {
    // Get the search term from the input field
    const searchTerm = $("#search-input").val();
    
    // Get the selected filter option
    const filterBy = $("#filter-select").val();

    // Make an AJAX request to the search endpoint
    $.ajax({
        type: "POST",
        url: "/receptionist/search-appointments/",
        headers: {
            "X-CSRFToken": "{{ csrf_token() }}", // Include the CSRF token in the headers
        },
        data: JSON.stringify({ searchTerm: searchTerm, filterBy: filterBy }),
        contentType: "application/json", // Set content type to JSON
        success: function (data) {
            // Update the table with the new data
            updateTableWithData(data);
        },
        error: function (error) {
            console.error("Error while making the search request:", error);
            alert("Error while making the search request. Please check the server response.");
        },
    });
  });

  // Function to update the table with new data
  function updateTableWithData(data) {
    // Get the table body element
    var tableBody = $("tbody");

    // Clear existing rows
    tableBody.empty();

    // Iterate over the data and append new rows to the table
    for (var i = 0; i < data.length; i++) {
        var row = data[i];
        var newRow = $("<tr>");
        newRow.append("<td class='doccare-reference-number'>" + row.reference_number + "</td>");
        newRow.append("<td>" + row.date_appointment + "</td>");
        newRow.append("<td>" + row.time_appointment + "</td>");
        newRow.append("<td><div class='status-cell'><p class='status'><strong>" + row.status_ + "</strong></p></div></td>");
        newRow.append("<td class='table__cell'><a href='/receptionist/view_appointment?reference_number=" + row.reference_number + "' class='doccare-view-appoinment-icon'><span class='material-symbols-outlined'>info</span></a><a href='/receptionist/reschedule?reference_number=" + row.reference_number + "' class='doccare-edit-appoinment-icon'><span class='material-symbols-outlined'>edit</span></a><button type='button' class='delete-appoinment-button' data-id='" + row.reference_number + "' onclick='openDeleteModal(" + row.reference_number + ")'><span class='material-symbols-outlined delete-icon'>delete</span></button></td>");

        // Check if the appointment is canceled and disable the edit icon accordingly
        if (row.status_ === 'CANCELLED') {
            const editIcon = newRow.find('.doccare-edit-appoinment-icon');
            if (editIcon) {
                editIcon.addClass('disabled');
                editIcon.removeAttr('href');
            }
        }

        // Append the new row to the table body
        tableBody.append(newRow);
    }
}



// Selectors
const searchInput = document.querySelector('.doccare-input-group input');
const tableRows = document.querySelectorAll('tbody tr');
const tableHeadings = document.querySelectorAll('thead th');
const deleteModal = document.getElementById('deleteModal');
const cancelModal = document.getElementById('cancelModal');

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

    // Reset background color for even rows
    row.style.backgroundColor = i % 2 === 0 ? '#ecf6ff' : '';
  });

  setTimeout(() => {
    const visibleRows = document.querySelectorAll('tbody tr:not(.hide)');
    visibleRows.forEach((visibleRow, i) => {
      visibleRow.style.backgroundColor = i % 2 === 0 ? '#fff5' : '#ecf6ff';
    });
  }, 300); // Adjust the delay to match the transition duration
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
  const appointmentId = deleteModal.getAttribute('data-appointment-id');
  const csrfToken = document.querySelector('meta[name="csrf-token"]').content;

  // Make an AJAX request to delete the appointment
  $.ajax({
      type: 'POST',
      url: '/receptionist/cancel-appointment/',
      data: { reference_number: appointmentId },
      headers: {
          "X-CSRFToken": csrfToken, // Include the CSRF token in the headers
      },
      success: function (response) {
          // Check the response from the server
          if (response.success) {
              // Update the table with the new data
              updateTableWithData(response.appointments);

              // Display a success message or handle as needed
              alert('Appointment cancelled successfully!');
          } else {
              // Display an error message or handle as needed
              alert('Failed to cancel appointment.');
          }

          // Close the cancel modal
          closeCancelModal();
      },
      error: function () {
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
