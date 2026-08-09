const ctx = document.getElementById('pieChart').getContext('2d');
let dy_list_count = [];
let dy_list_label = [];
Chart.defaults.font.size = 16;
Chart.register(ChartDataLabels);
const config = {
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
};

new Chart(ctx, config);

function drawChart(data) {
    /* Maintaining the filter options above the download button opens here */
    let dy_list_count = [];
    let dy_list_label = [];
    let totalSum = 0;
    let finalHTML1 = "";
    if (Array.isArray(data)) {
        data.forEach((element, index) => {
            totalSum += element.count;
            dy_list_count.push(element.count);
            dy_list_label.push(element.category_display);
        })
    }
    /* Maintaining the filter options above the download button ends here */

    // const download_link = document.getElementById('excel-download');
    /* Updates the entire chart data -starts- */
    const existingChart = Chart.getChart("pieChart");
    if (existingChart) existingChart.destroy();
    config.data.datasets[0].data = dy_list_count;
    config.data.labels = dy_list_label;
    new Chart(ctx, config);
    document.getElementById('total_count').innerHTML = 'Total Forms Filled are: ' + totalSum;
    /* Updates the entire chart data -ends- */
}

