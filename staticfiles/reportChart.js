const ctx = document.getElementById('pieChart').getContext('2d');
let dy_list_count = [];
let dy_list_label = [];
const data = JSON.parse(document.getElementById(`data-form-${form_number[0]}`).textContent);
var totalSum = 0;
let finalHTML1 = "";
if(Array.isArray(data)) {
    data.forEach((element, index) => {
        totalSum += element.count;
        dy_list_count.push(element.count);
        dy_list_label.push(element.category_display);
        finalHTML1 += `
              <div class = "form-check ms-2" >
                  <input type = "checkbox" class = "form-check-input" id = "check${index}" name = "optcheck[]" value = "${element.category}" style = "border: 2px solid black;">
                  <label class = "form-check-label" for = "check${index}"><b>${element.category_display}</b></label>
              </div>
            `
        })
        document.getElementById("checkBoxGroup").innerHTML = finalHTML1;
} else {
      dy_list_count.push(data);
      totalSum += data;
      if (form_number.includes('1_1')) {
        dy_list_label.push('Faculty Profile Details');
        document.getElementById("checkBoxGroup").innerHTML = `
          <div class = "form-check ms-2">
              <input type = "checkbox" class = "form-check-input" id = "check1" name = "optcheck[]" value = "CSE" style = "border: 2px solid black;">
              <label class = "form-check-label" for = "check1"><b>CSE</b></label>
          </div>
          <div class = "form-check ms-2">
              <input type = "checkbox" class = "form-check-input" id = "check2" name = "optcheck[]" value = "CSE(AI)" style = "border: 2px solid black;">
              <label class = "form-check-label" for = "check2"><b>CSE(AI)</b></label>
          </div>
          <div class = "form-check ms-2">
              <input type = "checkbox" class = "form-check-input" id = "check3" name = "optcheck[]" value = "CSE(DS)" style = "border: 2px solid black;">
              <label class = "form-check-label" for = "check3"><b>CSE(DS)</b></label>
          </div>
          <div class = "form-check ms-2">
              <input type = "checkbox" class = "form-check-input" id = "check4" name = "optcheck[]" value = "CSE(IOT)" style = "border: 2px solid black;">
              <label class = "form-check-label" for = "check4"><b>CSE(IOT)</b></label>
          </div>
        `
      } else if(form_number.includes('1_2')) {
        dy_list_label.push('Non-Teaching Staff');
        document.getElementById("checkBoxGroup").innerHTML = `
          <div class = "form-check ms-2">
              <input type = "checkbox" class = "form-check-input" id = "check1" name = "optcheck[]" value = "" style = "border: 2px solid black;">
              <label class = "form-check-label" for = "check1"><b>All</b></label>
          </div>
        `
      } else if(form_number.includes('7_1')) {
        dy_list_label.push('Research Publication - Journals');
        document.getElementById("checkBoxGroup").innerHTML = `
          <div class = "form-check ms-2">
              <input type = "checkbox" class = "form-check-input" id = "check1" name = "optcheck[]" value = "S" style = "border: 2px solid black;">
              <label class = "form-check-label" for = "check1"><b>SCI/SCIE/SSCI</b></label>
          </div>
          <div class = "form-check ms-2">
              <input type = "checkbox" class = "form-check-input" id = "check2" name = "optcheck[]" value = "NS" style = "border: 2px solid black;">
              <label class = "form-check-label" for = "check2"><b>Scopus</b></label>
          </div>
          <div class = "form-check ms-2">
              <input type = "checkbox" class = "form-check-input" id = "check3" name = "optcheck[]" value = "ES" style = "border: 2px solid black;">
              <label class = "form-check-label" for = "check3"><b>ESCI</b></label>
          </div>
          <div class = "form-check ms-2">
              <input type = "checkbox" class = "form-check-input" id = "check4" name = "optcheck[]" value = "UGC" style = "border: 2px solid black;">
              <label class = "form-check-label" for = "check4"><b>UGC</b></label>
          </div>
          <div class = "form-check ms-2">
              <input type = "checkbox" class = "form-check-input" id = "check4" name = "optcheck[]" value = "O" style = "border: 2px solid black;">
              <label class = "form-check-label" for = "check4"><b>Other</b></label>
          </div>
        `
      } else if(form_number.includes('7_2')) {
        dy_list_label.push('Research Publication - Conference Publication');
        document.getElementById("checkBoxGroup").innerHTML = `
          <div class = "form-check ms-2">
              <input type = "checkbox" class = "form-check-input" id = "check1" name = "optcheck[]" value = "Na" style = "border: 2px solid black;">
              <label class = "form-check-label" for = "check1"><b>National</b></label>
          </div>
          <div class = "form-check ms-2">
              <input type = "checkbox" class = "form-check-input" id = "check2" name = "optcheck[]" value = "In" style = "border: 2px solid black;">
              <label class = "form-check-label" for = "check2"><b>International</b></label>
          </div>
        `
      } else if(form_number.includes('7_3')) {
        dy_list_label.push('Research Publication - Book and Book Chapters');
        document.getElementById("checkBoxGroup").innerHTML = `
          <div class = "form-check ms-2">
              <input type = "checkbox" class = "form-check-input" id = "check1" name = "optcheck[]" value = "Na" style = "border: 2px solid black;">
              <label class = "form-check-label" for = "check1"><b>National</b></label>
          </div>
          <div class = "form-check ms-2">
              <input type = "checkbox" class = "form-check-input" id = "check2" name = "optcheck[]" value = "In" style = "border: 2px solid black;">
              <label class = "form-check-label" for = "check2"><b>International</b></label>
          </div>
        `
      } else if(form_number.includes('7_4')) {
        dy_list_label.push('Patents');
        document.getElementById("checkBoxGroup").innerHTML = `
          <div class = "row">
            <h6 class = "col text-center">Status of Patent: </h6>
            <div class = "col d-flex justify-content-center">
              <div class = "form-check ms-2">
                <input type = "checkbox" class = "form-check-input" id = "check1" name = "optcheck[]" value = "P" style = "border: 2px solid black;">
                <label class = "form-check-label" for = "check1"><b>Published</b></label>
              </div>
              <div class = "form-check ms-2">
                <input type = "checkbox" class = "form-check-input" id = "check2" name = "optcheck[]" value = "G" style = "border: 2px solid black;">
                <label class = "form-check-label" for = "check2"><b>Granted</b></label>
              </div>
            </div>
          </div>
          <div class = "row">
            <h6 class = "col text-center">Type of Patent: </h6>
            <div class = "col d-flex justify-content-center">  
              <div class = "form-check ms-2">
                <input type = "checkbox" class = "form-check-input" id = "check3" name = "optcheck[]" value = "I" style = "border: 2px solid black;">
                <label class = "form-check-label" for = "check3"><b>Innovation</b></label>
              </div>
              <div class = "form-check ms-2">
                <input type = "checkbox" class = "form-check-input" id = "check4" name = "optcheck[]" value = "D" style = "border: 2px solid black;">
                <label class = "form-check-label" for = "check4"><b>Design</b></label>
              </div>
            </div>  
          </div>
        `
      }
  }
document.getElementById('total_count').innerHTML = 'Total Forms Filled are: ' + totalSum;

Chart.defaults.font.size = 16;
Chart.register(ChartDataLabels);
let pieChart = new Chart(ctx, {
  type: 'pie',
  data: {
    labels: dy_list_label,
    datasets: [{
      data: dy_list_count,
      backgroundColor: ['#FFADAD', '#FFD6A5', '#FDFFB6', '#CAFFBF', '#9BF6FF', '#A0C4FF', '#BDB2FF', '#FFC6FF', '#E2E2E2', '#FFFFFC'],
      borderWidth: 1,
      borderColor: '#fff'
    }]
  },
  options: {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'top',
        labels: {
          font: {
            size: 16,
            family: 'Helvetica Neue',
            weight: 'bold'
          }
        }
      },
      title: {
        display: true,
        text: 'Overall Faculties Progress',
        position: 'top',
        padding: {
           bottom: 30
        }
      },
      datalabels: {
        formatter: (value, context) => {
          return value;
        },
        color: '#444', // Color of the text on the chart
        font: {
          weight: 'bold',
          size: 14
        },
        anchor: 'center', // Position: 'start', 'center', or 'end'
        align: 'center'
      }
    }
  }
});

const download_link = document.getElementById('excel-download');
document.querySelectorAll('.nav-link').forEach(link => {
     link.addEventListener('click', function(event) {
         totalSum = 0;
         const id = this.id;
         const data = JSON.parse(document.getElementById(`data-form-${id}`).textContent);
         let dy_list_count = [];
         let dy_list_label = [];
         let finalHTML = "";
         document.getElementById('filter').style.display = 'block';
         if(Array.isArray(data)) {
             data.forEach(element => {
                 totalSum += element.count;
                 dy_list_count.push(element.count);
                 dy_list_label.push(element.category_display);
                 finalHTML += `
                    <div class = "form-check ms-2" >
                        <input type = "checkbox" class = "form-check-input" id = "check${totalSum}" name = "optcheck[]" value = "${element.category}" style = "border: 2px solid black;">
                        <label class = "form-check-label" for = "check1"><b>${element.category_display}</b></label>
                    </div>
                 `
             })
             document.getElementById("checkBoxGroup").innerHTML = finalHTML;
         } else {
              dy_list_count.push(data);
              totalSum += data;
              if(id === '1_2') {
                dy_list_label.push('Non-Teaching Staff');
                document.getElementById("checkBoxGroup").innerHTML = `
                  <div class = "form-check ms-2">
                      <input type = "checkbox" class = "form-check-input" id = "check1" name = "optcheck[]" value = "" style = "border: 2px solid black;">
                      <label class = "form-check-label" for = "check1"><b>All</b></label>
                  </div>
                `
              }
         }
        pieChart.data.datasets[0].data = dy_list_count;
        pieChart.data.labels = dy_list_label;
        pieChart.update();
        document.getElementById('total_count').innerHTML = 'Total Forms Filled are: ' + totalSum;
        // Filteration method
        const downloadButton = document.getElementById(`download-button-${id}`);
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
        // const isChecked = Array.from(checkboxs).some(cb => cb.checked);
        //         downloadButton.disabled = !isChecked;
        //         const selCheckVal = Array.from(checkboxs).filter(cb => cb.checked).map(cb => cb.value);
        //         console.log(selCheckVal);
        //         const formData = new FormData();
        //         selCheckVal.forEach(value => {
        //             formData.append('optcheck[]', value);
        //         });
        //         formData.append('form_no',id);
        //         fetch('/download', {
        //             method: 'POST',
        //             headers: { 'X-CSRFToken': getCookie('csrftoken') },
        //             body: formData
        //         })
        //         .then(response => response.text())
        //         .catch(error => {
        //             console.error('Error is: ', error);
        //         });
        cleanDownloadButton.addEventListener('click', function() {
            
            const selCheckVal = Array.from(currentCheckboxes)
                .filter(cb => cb.checked)
                .map(cb => cb.value);

            const formData = new FormData();
            selCheckVal.forEach(value => {
                formData.append('optcheck[]', value);
            });
            formData.append('form_no', id);

            fetch('/download', {
                method: 'POST',
                headers: { 'X-CSRFToken': getCookie('csrftoken') },
                body: formData
            })
            .then(response => response.text())
            .catch(error => {
                console.error('Error is: ', error);
            });
        });
   });
});

const downloadButton = document.getElementById(`download-button-${form_number[0]}`);
const checkboxs = document.querySelectorAll('.form-check-input');
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
cleanDownloadButton.addEventListener('click', function(e) {
    
    const selCheckVal = Array.from(currentCheckboxes)
        .filter(cb => cb.checked)
        .map(cb => cb.value);

    const formData = new FormData();
    selCheckVal.forEach(value => {
        formData.append('optcheck[]', value);
    });
    formData.append('form_no', form_number[0]);

    fetch('/download', {
        method: 'POST',
        headers: { 'X-CSRFToken': getCookie('csrftoken') },
        body: formData
    })
    .then(response => response.text())
    .catch(error => {
        console.error('Error is: ', error);
    });
});

// Helper function to get the CSRF token from cookies
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

