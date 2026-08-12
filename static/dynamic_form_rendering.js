const loadingTableStructure = `
    <div class="table-responsive pt-2" id="dynamic_table">
        <table class = "table table-hover table-striped mt-3" id="loading_table">
            <tbody>
                 <tr>
                    <td class="d-flex justify-content-center">
                        <div class="spinner-border text-primary text-center" role="status">
<!--                            <span class="sr-only">Loading...</span>-->
                        </div><span class="ms-2">Loading Data...</span>
                    </td>
                 </tr>
            </tbody>
        </table>
    </div>
`;

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
function updateTable(values, table_id) {
    const table_to_update = document.getElementById('dynamic_table');
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
                table_html_structure += `<td><a href = "forms_listing/progressdetails/${table_id}/${row_val[col_val]}" style = "text-decoration: none; color: black;"><i class="fa-solid fa-pen"></i></a></td>`;
            } else if (col_val.includes('(File)')){
                if (row_val[col_val] !== 'Not Uploaded Yet') {
                    table_html_structure += `<td><a href="/media/${row_val[col_val]}" target="_blank" class="text-info">Click Here</a></td>`
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
                    <td><a href = "#" data-bs-toggle="modal" data-bs-target="#deleteUser" data-form_no = "${table_id}" data-pk = "${row_val['Edit']}" data-emp-id = "${row_val['Employee ID']}" data-head-main = "Employee Email" data-head-main-entry = "${row_val['Email']}" data-sub-head = "Employee Name" data-sub-head-entry = "${row_val['Name']}" style = "text-decoration: none; color: black;"><i class="fa-solid fa-trash-can"></i></a></td>
                </tr>`;
            } else if (table_id === '2') {
                table_html_structure += `
                    <td><a href = "#" data-bs-toggle="modal" data-bs-target="#deleteUser" data-form_no = "${table_id}" data-pk = "${row_val['Edit']}" data-emp-id = "${row_val['Employee ID']}" data-head-main = "Name of Faculty Member" data-head-main-entry = "${row_val['Name of Faculty Member']}" data-sub-head = "Title of Program" data-sub-head-entry = "${row_val['Title Of Program']}" style = "text-decoration: none; color: black;"><i class="fa-solid fa-trash-can"></i></a></td>
                </tr>`;
            } else if (table_id === '3') {
                table_html_structure += `
                    <td><a href = "#" data-bs-toggle="modal" data-bs-target="#deleteUser" data-form_no = "${table_id}" data-pk = "${row_val['Edit']}" data-emp-id = "${row_val['Employee ID']}" data-head-main = "Name of Faculty Member" data-head-main-entry = "${row_val['Name of Faculty Member']}" data-sub-head = "Name of the Course" data-sub-head-entry = "${row_val['Name of the Course']}" style = "text-decoration: none; color: black;"><i class="fa-solid fa-trash-can"></i></a></td>
                </tr>`;
            } else if (table_id === '4') {
                table_html_structure += `
                    <td><a href = "#" data-bs-toggle="modal" data-bs-target="#deleteUser" data-form_no = "${table_id}" data-pk = "${row_val['Edit']}" data-emp-id = "${row_val['Employee ID']}" data-head-main = "Name of the Faculty Coordinator" data-head-main-entry = "${row_val['Name of Faculty Coordinator(s)']}" data-sub-head = "Title of the Professional Development Program Organized" data-sub-head-entry = "${row_val['Title of the Professional Development Program Organized']}" style = "text-decoration: none; color: black;"><i class="fa-solid fa-trash-can"></i></a></td>
                </tr>`;
            } else if (table_id === '5') {
                table_html_structure += `
                    <td><a href = "#" data-bs-toggle="modal" data-bs-target="#deleteUser" data-form_no = "${table_id}" data-pk = "${row_val['Edit']}" data-emp-id = "${row_val['Employee ID']}" data-head-main = "Faculty Name" data-head-main-entry = "${row_val['Faculty Name']}" data-sub-head = "Name of Award/Achievement" data-sub-head-entry = "${row_val['Name of Award/Achievement']}" style = "text-decoration: none; color: black;"><i class="fa-solid fa-trash-can"></i></a></td>
                </tr>`;
            } else if (table_id === '6') {
                table_html_structure += `
                    <td><a href = "#" data-bs-toggle="modal" data-bs-target="#deleteUser" data-form_no = "${table_id}" data-pk = "${row_val['Edit']}" data-emp-id = "${row_val['Employee ID']}" data-head-main = "Name of Candidate (PI/Co PI)" data-head-main-entry = "${row_val['Name of Candidate (PI/Co PI)']}" data-sub-head = "Name of the Funding Agency" data-sub-head-entry = "${row_val['Name of the Funding Agency(MSME/DST/CSIR/SERB /Industry etc.)']}" style = "text-decoration: none; color: black;"><i class="fa-solid fa-trash-can"></i></a></td>
                </tr>`;
            } else if (table_id === '7_1') {
                table_html_structure += `
                    <td><a href = "#" data-bs-toggle="modal" data-bs-target="#deleteUser" data-form_no = "${table_id}" data-pk = "${row_val['Edit']}" data-emp-id = "${row_val['Employee ID']}" data-head-main = "Name of the author(s)" data-head-main-entry = "${row_val['Name of the author(s)']}" data-sub-head = "Title of Paper" data-sub-head-entry = "${row_val['Title of Paper']}" style = "text-decoration: none; color: black;"><i class="fa-solid fa-trash-can"></i></a></td>
                </tr>`;
            } else if (table_id === '7_2') {
                table_html_structure += `
                    <td><a href = "#" data-bs-toggle="modal" data-bs-target="#deleteUser" data-form_no = "${table_id}" data-pk = "${row_val['Edit']}" data-emp-id = "${row_val['Employee ID']}" data-head-main = "Name of the author(s)" data-head-main-entry = "${row_val['Name of the author(s)']}" data-sub-head = "Title of Conference" data-sub-head-entry = "${row_val['Title of Conference']}" style = "text-decoration: none; color: black;"><i class="fa-solid fa-trash-can"></i></a></td>
                </tr>`;
            } else if (table_id === '7_3') {
                table_html_structure += `
                    <td><a href = "#" data-bs-toggle="modal" data-bs-target="#deleteUser" data-form_no = "${table_id}" data-pk = "${row_val['Edit']}" data-emp-id = "${row_val['Employee ID']}" data-head-main = "Name of the author/editor" data-head-main-entry = "${row_val['Name of the author/editor']}" data-sub-head = "Title of the book" data-sub-head-entry = "${row_val['Title of the book']}" style = "text-decoration: none; color: black;"><i class="fa-solid fa-trash-can"></i></a></td>
                </tr>`;
            } else if (table_id === '7_4') {
                table_html_structure += `
                    <td><a href = "#" data-bs-toggle="modal" data-bs-target="#deleteUser" data-form_no = "${table_id}" data-pk = "${row_val['Edit']}" data-emp-id = "${row_val['Employee ID']}" data-head-main = "Name of Faculty" data-head-main-entry = "${row_val['Name of Faculty']}" data-sub-head = "Title of Patent" data-sub-head-entry = "${row_val['Title of Patent']}" style = "text-decoration: none; color: black;"><i class="fa-solid fa-trash-can"></i></a></td>
                </tr>`;
            } else if (table_id === '8') {
                table_html_structure += `
                    <td><a href = "#" data-bs-toggle="modal" data-bs-target="#deleteUser" data-form_no = "${table_id}" data-pk = "${row_val['Edit']}" data-emp-id = "${row_val['Employee ID']}" data-head-main = "Faculty Name" data-head-main-entry = "${row_val['Faculty Name']}" data-sub-head = "Name of the student Guided" data-sub-head-entry = "${row_val['Name of the student Guided']}" style = "text-decoration: none; color: black;"><i class="fa-solid fa-trash-can"></i></a></td>
                </tr>`;
            } else if (table_id === '9') {
                table_html_structure += `
                    <td><a href = "#" data-bs-toggle="modal" data-bs-target="#deleteUser" data-form_no = "${table_id}" data-pk = "${row_val['Edit']}" data-emp-id = "${row_val['Employee ID']}" data-head-main = "Name of Faculty Member" data-head-main-entry = "${row_val['Name of Faculty Member']}" data-sub-head = "Resource Person in" data-sub-head-entry = "${row_val['Resource Person in']}" style = "text-decoration: none; color: black;"><i class="fa-solid fa-trash-can"></i></a></td>
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
}

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.startsWith(name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

function fixLastColumn(containerId) {
    const tagId = 'my-dynamic-style-tag';
    if (containerId !== '1_1') {
        if (!document.getElementById(tagId)) {
            const styleTag = document.createElement('style');
            styleTag.id = tagId;
            styleTag.textContent = `
            table.dataTable thead th:last-child {
                position: sticky;
                right: 0;
                z-index: 10; /* Keep on top of other headers */
                background-color: #000000;
                box-shadow: -2px 0 5px rgba(0, 0, 0, 0.1); /* Optional shadow for depth */
            }
    
            /* Fix the Last Column in the Body */
            table.dataTable tbody td:last-child {
                position: sticky;
                right: 0;
                z-index: 9;
                background-color: #fff; /* MUST be set, or text will overlap transparently */
                box-shadow: -2px 0 5px rgba(0, 0, 0, 0.1); /* Optional shadow */
            }

            table.dataTable tbody tr.dataTables_empty td {
                text-align: left !important;
                padding-left: 1rem;
            }
        `;
            document.head.appendChild(styleTag);
        }
    } else {
        const existingTag = document.getElementById(tagId);
        if (existingTag) {
            existingTag.remove(); // Removes the tag and kills the styles instantly
        }
    }
}

// Maping of each nav-tabs all dropdown and text based inputs form number wise
const TAB_FILTER_CONFIG = {
    '1_1': {
        text: [{'Employee ID' : 'emp_id'}, {'Email': 'email'}, {'Name' : 'name'}],
        dropdown: [{'Department' : 'department'}, {'Designation' : 'designation'}],
        radio: [{'Session' : 'session'}]
    },
    '1_2': {
        text: [{'Employee ID' : 'emp_id'}, {'Email': 'email'}, {'Name' : 'name'}],
        dropdown: [{'Department' : 'department'}, {'Designation' : 'designation'}, {'Highest Qualfication' : 'highest'}, {'Professional Courses' : 'professional_course'}],
        radio: [{'Session' : 'session'}]
    },
    '2': {
        text: [{'Employee ID' : 'emp_id'}, {'Email': 'email'}, {'Name of Faculty Member' : 'name'}],
        dropdown: [{'Department' : 'department'}, {'Designation' : 'designation'}, {'Mode': 'mode'}, {'Level' :'level'}, {'Grant Recieved from SKIT (Yes/No)' : 'grant'}, {'Conference/FDP/ Workshop/Seminar/ STTP' : 'optcheck'}],
        radio: [{'Session' : 'session'}]
    },
    '3': {
        text: [{'Employee ID' : 'emp_id'}, {'Email address': 'email'}, {'Name of Faculty Member' : 'name'}],
        dropdown: [{'Duration of Course' : 'duration'}, {'Department' : 'department'}, {'Designation' : 'designation'}, {'Certificate Type' : 'certificate'}, {'Any category from below' : 'topper'}, {'Type of Course' : 'optcheck'}],
        radio: [{'Session' : 'session'}]
    },
    '4': {
        text: [{'Employee ID' : 'emp_id'}, {'Email address': 'email'}, {'Name of Faculty Coordinator(s)' : 'name'}],
        dropdown: [{'Department' : 'department'}, {'Designation' : 'designation'}, {'Event organized for' : 'event_org_for'}, {'Sponsored/Non Sponsored' : 'spo_non_spo'},
            {'Grant Received(Yes/No)' : 'grant'}, {'Type of Event' : 'optcheck'},{"Mapped SDG's" : 'map'}],
        radio: [{'Session' : 'session'}]
    },
    '5': {
        text: [{'Employee ID' : 'emp_id'}, {'Email address': 'email'}, {'Faculty Name' : 'name'}],
        dropdown: [{'Department' : 'department'}, {'Designation' : 'designation'}, {'Category' : 'optcheck'}],
        radio: [{'Session' : 'session'}, {'Employee ID' : 'emp_id'}, {'Email address': 'email'}, {'Faculty Name' : 'name'}]
    },
    '6': {
        text: [{'Employee ID' : 'emp_id'}, {'Email address': 'email'}, {'Name of Candidate (PI/Co PI)' : 'name'}],
        dropdown: [{'Department' : 'department'}, {'Designation' : 'designation'}, {'Status' :'status'}, {'Category' : 'optcheck'}],
        radio: [{'Session' : 'session'}]
    },
    '7_1': {
        text: [{'Employee ID' : 'emp_id'}, {'Email address': 'email'}, {'Name of the author(s)' : 'name'}],
        dropdown: [{'Department' : 'department'}, {'Designation' : 'designation'}, {'Level (National/ International)' : 'level'}, {'Indexed by' : 'optcheck'},
            {'Quartile' : 'quartile'}, {'Is SKIT student associated?' : 'ssa'}],
        radio: [{'Session' : 'session'}]
    },
    '7_2': {
        text: [{'Employee ID' : 'emp_id'}, {'Email address': 'email'}, {'Name of the author(s)' : 'name'}],
        dropdown: [{'Department' : 'department'}, {'Designation' : 'designation'}, {'Level (National/ International)' : 'optcheck'}, {'Is SKIT student associated?' : 'ssa'}],
        radio: [{'Session' : 'session'}]
    },
    '7_3': {
        text: [{'Employee ID' : 'emp_id'}, {'Email address': 'email'}, {'Name of the author/editor' : 'name'}],
        dropdown: [{'Department' : 'department'}, {'Designation' : 'designation'}, {'Level (National/ International)' : 'optcheck'}, {'Is SKIT student associated?' : 'ssa'}],
        radio: [{'Session' : 'session'}]
    },
    '7_4': {
        text: [{'Employee ID' : 'emp_id'}, {'Email address': 'email'}, {'Name of Faculty' : 'name'}],
        dropdown: [{'Department' : 'department'}, {'Designation' : 'designation'}, {'Status of Patent' : 'status'}, {'Type of Patent' : 'optcheck'}, {'Is SKIT student associated?' : 'ssa'}],
        radio: [{'Session' : 'session'}]
    },
    '8': {
        text: [{'Employee ID' : 'emp_id'}, {'Email address': 'email'}, {'Faculty Name' : 'name'}],
        dropdown: [{'Department' : 'department'}, {'Designation' : 'designation'}, {'Enrollment Year of Student' : 'eys'}, {'Supervisor / Co-supervisor' : 'visor'}, {'Program of Student' : 'optcheck'}],
        radio: [{'Session' : 'session'}]
    },
    '9': {
        text: [{'Employee ID' : 'emp_id'}, {'Email address': 'email'}, {'Name of Faculty Member' : 'name'}],
        dropdown: [{'Department' : 'department'}, {'Designation' : 'designation'}, {'Resource Person Type' : 'rpt'}, {'Resource Person in' : 'optcheck'}],
        radio: [{'Session' : 'session'}]
    }
};

// use for building table filters

function buildTableFilters(rowValues, tableId) {
    const container = document.getElementById('filterFieldsContainer');
    container.innerHTML = '';

    const config = TAB_FILTER_CONFIG[tableId];
    if (!config || !rowValues || rowValues.length === 0) return;

    const sampleRow = rowValues[0];
    let html = '';

    (config.text || []).forEach(item => {
        let [colKey, fieldName] = Object.entries(item)[0];
        if (!(colKey in sampleRow)) return; // column not present for this data, skip silently
        if (colKey === 'Name of Faculty Coordinator(s)') colKey = 'Faculty Coordinator Name';
        html += `
            <div class="col-md-3 mb-2">
                <label class="form-label">${colKey}</label>
                <input type="text" class="form-control filter-input" data-column="${colKey}" placeholder="Search ${colKey}" name="${fieldName}_filter">
            </div>`;
    });

    (config.radio || []).forEach(item => {
        let [colKey, fieldName] = Object.entries(item)[0];
        if (!(colKey in sampleRow)) return; // column not present for this data, skip silently
        const uniqueVals = [
            ...new Set(
                rowValues
                    .flatMap(r => (r[colKey] ? String(r[colKey]).split(',') : []))
                    .map(v => v.trim())
                )
            ].filter(Boolean).sort();

        let options = '';
        uniqueVals.forEach(((v, idx) => {
            const inputId = `filter_session_${idx}`;

            options += `
                <div class="form-check">
                    <label class="form-check-label small">
                        <input class="form-check-input filter-radio" type="radio" name="${fieldName}_filter" value="${v}" id="${inputId}">
                        ${v}
                    </label>
                </div>
            `;
        }));
        const reducedName = colKey.split('(')[0].trim();

        html += `
            <div class="col-md-3 mb-2">
                <label class="form-label">${reducedName}</label>
                <div class="dropdown filter-container">
                    <button type="button" 
                    class="btn btn-white btn-sm border w-100 dropdown-toggle text-start d-flex justify-content-between align-items-center bg-white dropdown-label-btn text-truncate overflow-hidden" 
                    data-bs-toggle="dropdown" data-bs-auto-close="outside" style="height: 38px;">
                        Select...
                    </button>
                    <ul class="dropdown-menu p-2 shadow-sm filter-radio" id="form_dropdown" data-column="${colKey}">
                        <li>${options}</li>
                    </ul>
                </div>
            </div>`;
    });

    (config.dropdown || []).forEach(item => {
        const [colKey, fieldName] = Object.entries(item)[0];
        if (!(colKey in sampleRow)) return;
        const uniqueVals = [
            ...new Set(
                rowValues
                    .flatMap(r => (r[colKey] ? String(r[colKey]).split(',') : []))
                    .map(v => v.trim())
                )
            ].filter(Boolean).sort();

        const sanitizedCol = colKey.replace(/[ ()/\-]/g, '_').toLowerCase();
        const nameParameter = fieldName + '_filter[]';

        let options = '';
        uniqueVals.forEach(((v, idx) => {
            const inputId = `filter_${sanitizedCol}_${idx}`;
            options += `
                <div class="form-check">
                    <input class="form-check-input filter-checkbox" type="checkbox" name="${nameParameter}" value="${v}" id="${inputId}">
                    <label class="form-check-label small" for="${inputId}">${v}</label>
                </div>
            `;
        }));
        const reducedName = colKey.split('(')[0].trim();

        html += `
            <div class="col-md-3 mb-2">
                <label class="form-label">${reducedName}</label>
                <div class="dropdown filter-container">
                    <button type="button" 
                    class="btn btn-white btn-sm border w-100 dropdown-toggle text-start d-flex justify-content-between align-items-center bg-white dropdown-label-btn text-truncate overflow-hidden" 
                    data-bs-toggle="dropdown" data-bs-auto-close="outside" style="height: 38px;">
                        Select...
                    </button>
                    <ul class="dropdown-menu p-2 shadow-sm filter-dropdown" id="form_dropdown" data-column="${colKey}">
                        <li>${options}</li>
                    </ul>
                </div>
            </div>`;
    });

    container.innerHTML = html;
}

// To update the dropdown value of all filter values in filter modal
// Attach a single listener to the document (or wrapper container)
document.addEventListener('change', function (e) {
    // Check if the changed element is one of our filter checkboxes
    if (e.target.classList.contains('filter-checkbox')) {

        // 1. Find the parent dropdown wrapper container for THIS specific filter
        const dropdownContainer = e.target.closest('.filter-container');
        if (!dropdownContainer) return;

        // 2. Find the target toggle button inside THIS container
        const labelBtn = dropdownContainer.querySelector('.dropdown-label-btn');

        // 3. Find all currently checked checkboxes inside THIS container
        const checkedBoxes = Array.from(
            dropdownContainer.querySelectorAll('.filter-checkbox:checked')
        ).map(cb => cb.value);

        // 4. Update the button text dynamically
        if (checkedBoxes.length === 0) {
            labelBtn.textContent = 'Select...';
        } else if (checkedBoxes.length === 1) {
            labelBtn.textContent = checkedBoxes[0];
        } else {
            labelBtn.textContent = `${checkedBoxes[0]} + ${checkedBoxes.length - 1} more`;
        }
    } else if (e.target.classList.contains('filter-radio')) {

        // 1. Find the parent dropdown wrapper container for THIS specific filter
        const dropdownContainer = e.target.closest('.filter-container');
        if (!dropdownContainer) return;

        // 2. Find the target toggle button inside THIS container
        const labelBtn = dropdownContainer.querySelector('.dropdown-label-btn');

        // 3. Find all currently checked checkboxes inside THIS container
        const selectedRadio = dropdownContainer.querySelector('.filter-radio:checked')

        // 4. Update the button text dynamically
        if (!selectedRadio) {
            labelBtn.textContent = 'Select...';
        } else {
            labelBtn.textContent = selectedRadio.value;
        }
    }
});

// applying filter to the table
let curr_table_id = '1_1';
function applyTableFilters() {

    document.querySelectorAll('.filter-input').forEach(input => {
        const col = input.dataset.column;
        if (input.value.trim() !== '') {
            if (col === 'Employee ID') {
                table.column(`${col}:name`).search(`^${input.value.trim()}$`, true, false);
            } else {
                table.column(`${col}:name`).search(input.value.trim());
            }
        }
    });

    document.querySelectorAll('.filter-dropdown').forEach(select => {
        const col = select.dataset.column;
        const val = Array.from(select.querySelectorAll('input[type="checkbox"]:checked'))
                                .map(cb => cb.value);
        if (val.length === 0) {
            table.column(`${col}:name`).search('');
        } else {
            const escaped = val.map(v => v.replace(/[-\/\\^$*+?.()|[\]{}]/g, '\\$&'));
            // 1. Join values with pipe | to create an OR pattern: (SDG_1|SDG_2)
            // 2. Wrap with ^ and $ for exact matching per item
            const regexPattern = `(^|,\\s*)(${escaped.join('|')})(\\s*,|$)`;
            console.log(`Checkbox regexPattern with col name ${col} is: `,regexPattern);
            table.column(`${col}:name`).search(regexPattern, true, false);
        }
    });

    document.querySelectorAll('.filter-radio').forEach(select => {
        const col = select.dataset.column;
        const radioButton = select.querySelector('input[type="radio"]:checked');
        if (!radioButton) {
            table.column(`${col}:name`).search('');
        } else {
            const escaped = radioButton.value.replace(/[-\/\\^$*+?.()|[\]{}]/g, '\\$&');
            table.column(`${col}:name`).search(`^${escaped}$`, true, false);
        }
    });

    table.draw(); // to print the final filtered table

    // Preparing data to be attached with download Excel button
    const valuesToPass = {};
    const config = TAB_FILTER_CONFIG[curr_table_id];

    (config.dropdown || []).forEach(item => {
        // 1. Extract key and value from the item object (e.g. {'Department': 'department'})
        const [key, value] = Object.entries(item)[0];

        // 2. Store in output dictionary
        valuesToPass[value] = Array.from(
            document.querySelectorAll(`input[name="${value}_filter[]"]:checked`)
        ).map(cb => cb.value);
    });

    (config.radio || []).forEach(item => {
        const [key, value] = Object.entries(item)[0];
        let selValues;

        selValues = Array.from(document.querySelectorAll(`input[name='${value}_filter']:checked`)).map(cb => cb.value);

        valuesToPass[value] = selValues;
    });

    (config.text || []).forEach(item => {
        const [key, value] = Object.entries(item)[0];

        valuesToPass[value] = document.querySelector(`input[name='${value}_filter']`).value;
        console.log(valuesToPass[value]);
    });


    console.log("Final Expected Dictionary is:",valuesToPass);

    // Updating Download Filtered Excel Button status (Enable/Disable)
    const downloadButton = document.getElementById(`download-button-${curr_table_id}`);
    // To remove the previous choices attached with button while downloading.
    const cleanDownloadButton = downloadButton.cloneNode(true);
    downloadButton.replaceWith(cleanDownloadButton);

    const currentCheckboxes = document.querySelectorAll('input[type="radio"], input[type="checkbox"]');

    const updateButtonState = () => {
        const isChecked = Array.from(currentCheckboxes).some(cb => cb.checked);
        const textInputs = document.querySelectorAll('input[type="text"]');
        const haveInput = Array.from(textInputs).some(input => input.value.trim() !== '');
        cleanDownloadButton.disabled = (!isChecked && !haveInput) || table.rows({ filter: 'applied' }).count() === 0;
    };
    updateButtonState();

    cleanDownloadButton.addEventListener('click', function() {
        const formData = new FormData();
        Object.entries(valuesToPass).forEach(([key, values]) => {
            // console.log("VAlues are: ", key, values);
            if (Array.isArray(values) && values.length > 0) {

                // Check if the HTML element is a radio button in the DOM
                const isRadio = document.querySelector(`input[name="${key}_filter"][type="radio"]`) !== null;

                if (!isRadio) {
                    // Checkboxes: Send key[]
                    values.forEach(val => {
                        formData.append(`${key}_filter[]`, val);
                    });
                } else {
                    // Radio button && Input Tag: Send plain key
                    formData.set(`${key}_filter`, values[0]);
                }
            } else if (!Array.isArray(values)) {
                console.log("VAlues are: ", key, values);
                formData.set(`${key}_filter`, values);
            }
        });
        formData.append('form_no', curr_table_id);

        fetch('/download', {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: formData
        })
            .then(response => response.json())
            .then(data => {
                if (!data.success) {
                    console.log(data.success);
                    alert(data.message);
                }
            })
            .catch(error => {
                console.error('Error is: ', error);
            });
    });


}

// for modal funtioning

function applyTableFiltersAndClose() {
    applyTableFilters();
    const modalEl = document.getElementById('advanceFilterModal');
    const modalInstance = bootstrap.Modal.getInstance(modalEl);
    if (modalInstance) modalInstance.hide();
}

// for clearing the table filters applied earlier

function clearTableFilters() {
    const allFilters = document.querySelectorAll('.filter-checkbox, .filter-radio');
     document.querySelectorAll('.filter-input').forEach(input => input.value = '');

    allFilters.forEach(input => {
        if (input.checked) {
            input.checked = false;

            // 2. Fire a change event so your existing event listener updates the button text to 'Select...'
            input.dispatchEvent(new Event('change', { bubbles: true }));
        }
    });
    table.columns().every(function () {
        this.search('');
    });
    table.draw(); // to resore the existing table view again back
}

// exising code started

function openTab(containerId) {
    const targetContainerId = document.querySelector('.nav-link.active').id;
    const tableExist = document.getElementById(`tb_${targetContainerId}`);
    if (targetContainerId && tableExist) {
        const spinnerContainer = document.getElementById(`tb_${targetContainerId}`)
        spinnerContainer.innerHTML = loadingTableStructure;
    }

    document.querySelectorAll(".nav-link").forEach(btn => {
        btn.classList.remove("active");
    });

    const activeContainer = document.getElementById(containerId);
    activeContainer.classList.add("active");

    const downloadButton_to_change = document.querySelector('[id^="download-button"]');
    downloadButton_to_change.disabled = true;
    downloadButton_to_change.id = 'download-button-'+containerId;


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
            updateTable(responseData.row_values, containerId);
            buildTableFilters(responseData.row_values, containerId); // for table advance filter options
            drawChart(responseData.map_data);
            curr_table_id = containerId;
            // filterDataToDownload();
            fixLastColumn(containerId);
        } else {
            updateTable('', 'empty-table');
        }
    })
    .catch(error => console.error('Error during fetching data: ', error));
}

function updateTableWithFilters(currentCheckboxes, table_id) {
    const selCheckVal = Array.from(currentCheckboxes)
            .filter(cb => cb.checked)
            .map(cb => {
                // Find the label whose 'for' attribute matches this checkbox's 'id'
                const label = document.querySelector(`label[for="${cb.id}"]`);
                return label ? label.textContent.trim() : "";
            });

    // 1. Escape special regex characters like ( and )
    const escapedTerms = selCheckVal.map(function(term) {
        return term.replace(/[-\/\\^$*+?.()|[\]{}]/g, '\\$&');
    });

    // 2. Join with | and wrap tightly with ^ and $
    const exactRegexString = '^(' + escapedTerms.join('|') + ')$';

    const table_id_to_column_name = {'1_1' : 'Department', '1_2' : 'Department', '2' : 'Conference/FDP/ Workshop/Seminar/ STTP',
                                        '3' : 'Type of Course', '4' : 'Type of Event', '5' : 'Category', '6' : 'Category',
                                        '7_1' : 'Indexed by', '7_2' : 'Level (National/ International)', '7_3' : 'Level (National/ International)',
                                        '7_4' : 'Type of Patent', '8' : 'Program of Student', '9' : 'Resource Person in'}

    const column_name = table_id_to_column_name[table_id];
    if (selCheckVal.length === 0) {
        // Passing an empty string removes the filter entirely
        table.column(`${column_name}:name`).search('').draw();
    } else table.column(`${column_name}:name`).search(exactRegexString, true, false).draw();
    const pieChart = Chart.getChart("pieChart");
    if (!pieChart) {
        console.log(`No Chart instance found attached to canvas ID: pieChart`)
        return;
    }
    const labels = pieChart.data.labels;
    labels.forEach((label, index) => {
        const shouldBeVisible = !selCheckVal || selCheckVal.length === 0 ? true : selCheckVal.includes(label);

        const isCurrentlyVisible = pieChart.getDataVisibility(index);

        if (isCurrentlyVisible !== shouldBeVisible) {
            pieChart.toggleDataVisibility(index);
        }
    });
    pieChart.update();
}

function filterDataToDownload() {
    // Filteration method
    const downloadButtonID = document.querySelector(`.nav-link.active`).id;
    const downloadButton = document.getElementById(`download-button-${downloadButtonID}`);
    // To remove the previous choices attached with button while downloading.
    const cleanDownloadButton = downloadButton.cloneNode(true);
    downloadButton.replaceWith(cleanDownloadButton);

    // const currentCheckboxes = document.querySelectorAll('.form-check-input');

    const updateButtonState = () => {
        const isChecked = Array.from(currentCheckboxes).some(cb => cb.checked);
        cleanDownloadButton.disabled = !isChecked;
    };
    updateButtonState();

    currentCheckboxes.forEach(checkbox => {
        checkbox.addEventListener('change', (event) => {
            updateButtonState();
            updateTableWithFilters(currentCheckboxes, downloadButtonID);
        });
    });
    cleanDownloadButton.addEventListener('click', function () {

        const selCheckVal = Array.from(currentCheckboxes)
            .filter(cb => cb.checked)
            .map(cb => cb.value);

        const formData = new FormData();
        selCheckVal.forEach(value => {
            formData.append('optcheck[]', value);
        });
        formData.append('form_no', downloadButtonID);

        fetch('/download', {
            method: 'POST',
            headers: {'X-CSRFToken': getCookie('csrftoken')},
            body: formData
        })
            .then(response => response.text())
            .catch(error => {
                console.error('Error is: ', error);
            });
    });
}