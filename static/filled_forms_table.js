const noDataAvailableTableStructure = `
    <div class="table-responsive pt-2" id="dynamic_table">
        <table class = "table table-hover table-striped mt-3" id="empty_table">
            <thead class = "table-dark">
                    <tr>
                        <th class="text-center">No Data Available</th>
                    </tr>

            </thead>
            <tbody>
                 <tr>
                    <td class="text-center">No Data Available</td>
                 </tr>
            </tbody>
        </table>
    </div>
`;

let table = new DataTable(`#tb_empty`, {
    paging: false,
    scrollY: '260px',
    scrollX: true,
    dom: 'lrtip',
    language: {
        emptyTable: "No Data Available",
        zeroRecords: "No Data Found For The Selected Filters"
    }
    // searching: false
});

function updateTable(values, table_id, emailId) {
    const table_to_update = document.getElementById('filled_forms_dynamic_table');
    if (table_id === 'empty-table') {
        table_to_update.innerHTML = noDataAvailableTableStructure;
        table = new DataTable(`#empty_table`, {
            paging: false,
            scrollY: false,
            scrollX: false,
            dom: 'lrtip',
            language: {
                emptyTable: "No Data Available",
                zeroRecords: "No Data Found For The Selected Filters"
            }
            // searching: false
        });
        return;
    }
    let table_html_structure = `
        <table class = "table table-hover table-striped mt-3" id="tb_${table_id}">
            <thead class = "table-dark">
                <tr>
    `;
    const col_values = Object.keys(values[0]);
    col_values.forEach((col) => {
        table_html_structure += `<th data-name="${col}">${col}</th>`;
    })
    if (table_id !== '1_1') table_html_structure += `<th>Delete</th>`;
    table_html_structure += `
            </tr>
        </thead>
        <tbody>
    `;
    values.forEach((row_val) => {
        table_html_structure += `<tr>`;
        col_values.forEach((col_val) => {
            if (col_val === 'Edit') {
                table_html_structure += `<td><a href = "/forms_listing/progressdetails/${table_id}/${row_val[col_val]}" style = "text-decoration: none; color: black;"><i class="fa-solid fa-pen"></i></a></td>`;
            } else if (col_val.includes('(File)')){
                if (row_val[col_val] !== 'Not Uploaded Yet') {
                    table_html_structure += `<td><a href="${row_val[col_val]}" target="_blank" class="text-info">Click Here</a></td>`
                } else {
                    table_html_structure += `<td>${row_val[col_val]}</td>`;
                }
            } else {
                table_html_structure += `<td>${row_val[col_val]}</td>`;
            }
        });
        if (table_id !== '1_1') {
            if (table_id === '1_2') {
                table_html_structure += `
                    <td><a href = "#" data-bs-toggle="modal" data-bs-target="#deleteFormEntry" data-form_no = "${table_id}" data-pk = "${row_val['Edit']}" data-emp-id = "${row_val['Employee ID']}" data-head-main = "Employee Email" data-head-main-entry = "${row_val['Email']}" data-sub-head = "Employee Name" data-sub-head-entry = "${row_val['Name']}" style = "text-decoration: none; color: black;"><i class="fa-solid fa-trash-can"></i></a></td>
                </tr>`;
            } else if (table_id === '2') {
                table_html_structure += `
                    <td><a href = "#" data-bs-toggle="modal" data-bs-target="#deleteFormEntry" data-form_no = "${table_id}" data-pk = "${row_val['Edit']}" data-emp-id = "${row_val['Employee ID']}" data-head-main = "Name of Faculty Member" data-head-main-entry = "${row_val['Name of Faculty Member']}" data-sub-head = "Title of Program" data-sub-head-entry = "${row_val['Title Of Program']}" style = "text-decoration: none; color: black;"><i class="fa-solid fa-trash-can"></i></a></td>
                </tr>`;
            } else if (table_id === '3') {
                table_html_structure += `
                    <td><a href = "#" data-bs-toggle="modal" data-bs-target="#deleteFormEntry" data-form_no = "${table_id}" data-pk = "${row_val['Edit']}" data-emp-id = "${row_val['Employee ID']}" data-head-main = "Name of Faculty Member" data-head-main-entry = "${row_val['Name of Faculty Member']}" data-sub-head = "Name of the Course" data-sub-head-entry = "${row_val['Name of the Course']}" style = "text-decoration: none; color: black;"><i class="fa-solid fa-trash-can"></i></a></td>
                </tr>`;
            } else if (table_id === '4') {
                table_html_structure += `
                    <td><a href = "#" data-bs-toggle="modal" data-bs-target="#deleteFormEntry" data-form_no = "${table_id}" data-pk = "${row_val['Edit']}" data-emp-id = "${row_val['Employee ID']}" data-head-main = "Name of the Faculty Coordinator" data-head-main-entry = "${row_val['Name of Faculty Coordinator(s)']}" data-sub-head = "Title of the Professional Development Program Organized" data-sub-head-entry = "${row_val['Title of the Professional Development Program Organized']}" style = "text-decoration: none; color: black;"><i class="fa-solid fa-trash-can"></i></a></td>
                </tr>`;
            } else if (table_id === '5') {
                table_html_structure += `
                    <td><a href = "#" data-bs-toggle="modal" data-bs-target="#deleteFormEntry" data-form_no = "${table_id}" data-pk = "${row_val['Edit']}" data-emp-id = "${row_val['Employee ID']}" data-head-main = "Faculty Name" data-head-main-entry = "${row_val['Faculty Name']}" data-sub-head = "Name of Award/Achievement" data-sub-head-entry = "${row_val['Name of Award/Achievement']}" style = "text-decoration: none; color: black;"><i class="fa-solid fa-trash-can"></i></a></td>
                </tr>`;
            } else if (table_id === '6') {
                table_html_structure += `
                    <td><a href = "#" data-bs-toggle="modal" data-bs-target="#deleteFormEntry" data-form_no = "${table_id}" data-pk = "${row_val['Edit']}" data-emp-id = "${row_val['Employee ID']}" data-head-main = "Name of Candidate (PI/Co PI)" data-head-main-entry = "${row_val['Name of Candidate (PI/Co PI)']}" data-sub-head = "Name of the Funding Agency" data-sub-head-entry = "${row_val['Name of the Funding Agency(MSME/DST/CSIR/SERB /Industry etc.)']}" style = "text-decoration: none; color: black;"><i class="fa-solid fa-trash-can"></i></a></td>
                </tr>`;
            } else if (table_id === '7_1') {
                table_html_structure += `
                    <td><a href = "#" data-bs-toggle="modal" data-bs-target="#deleteFormEntry" data-form_no = "${table_id}" data-pk = "${row_val['Edit']}" data-emp-id = "${row_val['Employee ID']}" data-head-main = "Name of the author(s)" data-head-main-entry = "${row_val['Name of the author(s)']}" data-sub-head = "Title of Paper" data-sub-head-entry = "${row_val['Title of Paper']}" style = "text-decoration: none; color: black;"><i class="fa-solid fa-trash-can"></i></a></td>
                </tr>`;
            } else if (table_id === '7_2') {
                table_html_structure += `
                    <td><a href = "#" data-bs-toggle="modal" data-bs-target="#deleteFormEntry" data-form_no = "${table_id}" data-pk = "${row_val['Edit']}" data-emp-id = "${row_val['Employee ID']}" data-head-main = "Name of the author(s)" data-head-main-entry = "${row_val['Name of the author(s)']}" data-sub-head = "Title of Conference" data-sub-head-entry = "${row_val['Title of Conference']}" style = "text-decoration: none; color: black;"><i class="fa-solid fa-trash-can"></i></a></td>
                </tr>`;
            } else if (table_id === '7_3') {
                table_html_structure += `
                    <td><a href = "#" data-bs-toggle="modal" data-bs-target="#deleteFormEntry" data-form_no = "${table_id}" data-pk = "${row_val['Edit']}" data-emp-id = "${row_val['Employee ID']}" data-head-main = "Name of the author/editor" data-head-main-entry = "${row_val['Name of the author/editor']}" data-sub-head = "Title of the book" data-sub-head-entry = "${row_val['Title of the book']}" style = "text-decoration: none; color: black;"><i class="fa-solid fa-trash-can"></i></a></td>
                </tr>`;
            } else if (table_id === '7_4') {
                table_html_structure += `
                    <td><a href = "#" data-bs-toggle="modal" data-bs-target="#deleteFormEntry" data-form_no = "${table_id}" data-pk = "${row_val['Edit']}" data-emp-id = "${row_val['Employee ID']}" data-head-main = "Name of Faculty" data-head-main-entry = "${row_val['Name of Faculty']}" data-sub-head = "Title of Patent" data-sub-head-entry = "${row_val['Title of Patent']}" style = "text-decoration: none; color: black;"><i class="fa-solid fa-trash-can"></i></a></td>
                </tr>`;
            } else if (table_id === '8') {
                table_html_structure += `
                    <td><a href = "#" data-bs-toggle="modal" data-bs-target="#deleteFormEntry" data-form_no = "${table_id}" data-pk = "${row_val['Edit']}" data-emp-id = "${row_val['Employee ID']}" data-head-main = "Faculty Name" data-head-main-entry = "${row_val['Faculty Name']}" data-sub-head = "Name of the student Guided" data-sub-head-entry = "${row_val['Name of the student Guided']}" style = "text-decoration: none; color: black;"><i class="fa-solid fa-trash-can"></i></a></td>
                </tr>`;
            } else if (table_id === '9') {
                table_html_structure += `
                    <td><a href = "#" data-bs-toggle="modal" data-bs-target="#deleteFormEntry" data-form_no = "${table_id}" data-pk = "${row_val['Edit']}" data-emp-id = "${row_val['Employee ID']}" data-head-main = "Name of Faculty Member" data-head-main-entry = "${row_val['Name of Faculty Member']}" data-sub-head = "Resource Person in" data-sub-head-entry = "${row_val['Resource Person in']}" style = "text-decoration: none; color: black;"><i class="fa-solid fa-trash-can"></i></a></td>
                </tr>`;
            }
        } else table_html_structure += `</tr>`;
    });
    table_html_structure += `
            </tbody>
        </table>
    `;
    table_to_update.innerHTML = table_html_structure;
    table = new DataTable(`#tb_${table_id}`, {
        paging: false,
        scrollY: '260px',
        scrollX: true,
        dom: 'lrtip',
        language: {
            emptyTable: "No Data Available",
            zeroRecords: "No Data Found For The Selected Filters"
        }
        // searching: false
    });
    const colName = (table_id === '2') ? 'Email' : 'Email address';
    table.column(`${colName}:name`).search(emailId).draw();
}

const changeFormNumber = {
    '1' : '2',
    '2' : '3',
    '3' : '4',
    '4' : '5',
    '5' : '6',
    '6' : '7_1',
    '7' : '7_2',
    '8' : '7_3',
    '9' : '7_4',
    '10' : '8',
    '11' : '9'
}

function renderTable() {
    let containerId = window.location.href.substring(window.location.href.lastIndexOf('/') + 1);
    containerId = changeFormNumber[containerId];
    const emailId = document.getElementById('email').value;
    fetch('/forms_report', {
        method: 'POST',
        headers: {
            'Content-type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({
            'form_id': containerId
        })
    })
    .then(response=>response.json())
    .then(responseData => {
        if (responseData.success && responseData.row_values && responseData.row_values.length > 0) {
            updateTable(responseData.row_values, containerId, emailId);
        } else {
            updateTable('', 'empty-table');
        }
    })
    .catch(error => console.error('Error during fetching data: ', error));
}

document.addEventListener('DOMContentLoaded', () => {
    renderTable();
})