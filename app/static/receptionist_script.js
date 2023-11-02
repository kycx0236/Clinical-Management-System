const searchInput = document.querySelector('.doccare-input-group input');
const tableRows = document.querySelectorAll('tbody tr');
const table_headings = document.querySelectorAll('thead th');


searchInput.addEventListener('input', searchTable);

function searchTable() {
  const searchValue = searchInput.value.toLowerCase();

  tableRows.forEach((row, i) => {
    const rowData = row.textContent.toLowerCase();
    const isMatch = rowData.includes(searchValue);

    row.classList.toggle('hide', !isMatch);
    row.style.setProperty('--delay', i / 25 + 's');

    // Reset background color for even rows
    if (i % 2 === 0) {
      row.style.backgroundColor = '#ecf6ff';
    }
  });

  const visibleRows = document.querySelectorAll('tbody tr:not(.hide)');
  visibleRows.forEach((visibleRow, i) => {
    visibleRow.style.backgroundColor = i % 2 === 0 ? '#fff5' : '#ecf6ff';
  });
}

table_headings.forEach((head, i) => {
    let sort_asc = true;
    head.onclick = () => {
        table_headings.forEach(head => head.classList.remove('active'));
        head.classList.add('active');

        document.querySelectorAll('td').forEach(td => td.classList.remove('active'));
        tableRows.forEach(row => {
            row.querySelectorAll('td')[i].classList.add('active');
        })

        head.classList.toggle('asc', sort_asc);
        sort_asc = head.classList.contains('asc') ? false : true;

        sortTable(i, sort_asc);
    }
})


function sortTable(column, sort_asc) {
    [...tableRows].sort((a, b) => {
        let first_row = a.querySelectorAll('td')[column].textContent.toLowerCase(),
            second_row = b.querySelectorAll('td')[column].textContent.toLowerCase();

        return sort_asc ? (first_row < second_row ? 1 : -1) : (first_row < second_row ? -1 : 1);
    })
        .map(sorted_row => document.querySelector('tbody').appendChild(sorted_row));
}
