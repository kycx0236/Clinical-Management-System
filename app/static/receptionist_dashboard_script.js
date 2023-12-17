// Apply the Styles for STATUS at the start of the template
applyStatusStyles();

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