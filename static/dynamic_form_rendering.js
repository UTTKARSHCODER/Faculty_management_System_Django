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

new DataTable(`#tb_empty`, {
    paging: false,
    scrollY: '260px',
    scrollX: true
});
function updateTable(values, table_id) {
    const table_to_update = document.getElementById('dynamic_table');
    if (table_id === 'empty-table') {
        table_to_update.innerHTML = noDataAvailableTableStructure;
        new DataTable(`#empty_table`, {
            paging: false,
            scrollY: '260px',
            scrollX: true
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
        table_html_structure += `<th>${col}</th>`;
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
    new DataTable(`#tb_${table_id}`, {
        paging: false,
        scrollY: '260px',
        scrollX: true
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
        if(responseData.success) {
            updateTable(responseData.row_values, containerId);
            drawChart(responseData.map_data);
            filterDataToDownload();
            fixLastColumn(containerId);
        } else {
            updateTable('', 'empty-table');
        }
    })
    .catch(error => console.error('Error during fetching data: ', error));
}

function filterDataToDownload() {
    // Filteration method
    const downloadButtonID = document.querySelector(`.nav-link.active`).id;
    const downloadButton = document.getElementById(`download-button-${downloadButtonID}`);
    // To remove the previous choices attached with button while downloading.
    const cleanDownloadButton = downloadButton.cloneNode(true);
    downloadButton.replaceWith(cleanDownloadButton);

    const currentCheckboxes = document.querySelectorAll('.form-check-input');

    const updateButtonState = () => {
        const isChecked = Array.from(currentCheckboxes).some(cb => cb.checked);
        cleanDownloadButton.disabled = !isChecked;
    };
    updateButtonState();

    currentCheckboxes.forEach(checkbox => {
        checkbox.addEventListener('change', updateButtonState);
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