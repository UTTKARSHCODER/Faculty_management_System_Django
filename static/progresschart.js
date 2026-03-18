//Sample data
const data = JSON.parse(document.getElementById(`my-data-form_wise_count`).textContent);
const dataMap = {
  cum: []
};
dataMap.cum = data;
const color = {
    cum: ['rgba(44, 160, 44, 0.7)','rgba(188, 189, 34, 0.7)','rgba(214, 39, 40, 0.7)',
    'rgba(23, 190, 207, 0.7)','rgba(255, 127, 14, 0.7)','rgba(106, 90, 205, 0.7)',
    'rgba(72, 61, 139, 0.7)','rgba(123, 104, 238, 0.7)','rgba(255, 215, 0, 0.7)'
    ,'rgba(173, 255, 47, 0.7)','rgba(255, 140, 0, 0.7)']
}
const label = []
const categoryColors = {
    // Education & Academic Degrees (Blues)
    'mp': 'rgba(44, 127, 184, 0.7)',
    'EE(PG)': 'rgba(100, 143, 255, 0.7)',
    'EE(UG)': 'rgba(174, 199, 232, 0.7)',
    'EDU': 'rgba(158, 218, 229, 0.7)',

    // Research & Publications (Oranges/Purples)
    'RP': 'rgba(255, 127, 14, 0.7)',
    'REA': 'rgba(255, 187, 120, 0.7)',
    'IP': 'rgba(148, 103, 189, 0.7)',
    'JOU': 'rgba(197, 176, 213, 0.7)',

    // Training & Workshops (Greens)
    'FDP': 'rgba(44, 160, 44, 0.7)',
    'WKP': 'rgba(152, 223, 138, 0.7)',
    'STTP': 'rgba(34, 139, 34, 0.7)',
    'STC': 'rgba(102, 194, 165, 0.7)',
    'TRA': 'rgba(122, 163, 84, 0.7)',

    // Events & Conferences (Reds/Browns)
    'SEM': 'rgba(214, 39, 40, 0.7)',
    'SYM': 'rgba(255, 152, 150, 0.7)',
    'WEB': 'rgba(140, 86, 75, 0.7)',
    'CON': 'rgba(196, 156, 148, 0.7)',
    'NTS': 'rgba(127, 127, 127, 0.7)',

    // Technical & Professional (Yellows/Teals)
    'MOOC': 'rgba(188, 189, 34, 0.7)',
    'EL': 'rgba(219, 219, 141, 0.7)',
    'ET': 'rgba(225, 225, 0, 0.7)',
    'CONS': 'rgba(23, 190, 207, 0.7)',
    'INT': 'rgba(158, 218, 229, 0.7)',

    // Administration & Committees (Pinks/Greys)
    'BOS': 'rgba(227, 119, 194, 0.7)',
    'DRC': 'rgba(247, 182, 210, 0.7)',
    'HAT': 'rgba(127, 127, 127, 0.7)',

    // Extra-Curricular (Vibrant)
    'SPO': 'rgba(255, 215, 0, 0.7)',
    'SG': 'rgba(255, 69, 0, 0.7)',
    'LS': 'rgba(173, 255, 47, 0.7)',

    'PATENTS': 'rgba(255, 215, 0, 0.7)',   // Gold (Signifies value/innovation)
    'RPJ':     'rgba(106, 90, 205, 0.7)',  // Slate Blue (Academic Journal feel)
    'RPCP':    'rgba(72, 61, 139, 0.7)',   // Dark Slate Blue (Conference distinction)
    'RPB':     'rgba(123, 104, 238, 0.7)',  // Medium Slate Blue (Book chapter)
    'RP':      'rgba(255, 140, 0, 0.7)',   // Dark Orange (Project energy)

    // Fallback
    'OTH': 'rgba(179, 179, 179, 0.7)',
    'DEFAULT': 'rgba(210, 210, 210, 0.7)'
};

const ctx = document.getElementById('barChart').getContext('2d');
Chart.register(ChartDataLabels);
let barChart = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: ["Faculty Profile Details", "Non-teaching Staff", "Faculty Participation", "MOOC/Short-term Course", "Events", "Faculty Awards", "Sponsored Research", "Research Publication - Journal", "Research Publication - Confernece", "Research Publication - Books", "Patents", "M.Tech/Ph.D Guided", "Resource Person"],
      datasets: [{
        data: dataMap.cum,
        borderColor: color.cum,
        backgroundColor: color.cum,
        barThickness: 40,
        maxBarThickness: 50,
        borderWidth: 1,
        datalabels: {
            color: 'black',
            anchor: 'end',
            align: 'top'
        }
      }]
    },
    plugins: [ChartDataLabels],
    options: {
      scales: {
        y: {
          beginAtZero: true,
          grace: '10%'
        }
      },
      plugins: {
        legend: {
            display: false
        }
      }
    }
  });


document.getElementById('activityDropdown').addEventListener('change', function () {
  const selected = this.value;
  if (selected === "") {
    window.location.reload();
  }
  console.log(selected);
  const data = JSON.parse(document.getElementById(`my-data-${selected}`).textContent);
  let dy_list_count = [];
  let dy_list_label = [];
  let dy_list_short_label = [];
  if (Array.isArray(data)) {
      data.forEach(element => {
        dy_list_count.push(element.count);
        dy_list_label.push(element.category_display);
        dy_list_short_label.push(element.category);
      });
  } else {
      dy_list_count.push(data);
      if (selected === '7_1') {
        dy_list_label.push('Research Publication - Journals');
        dy_list_short_label.push('RPJ');
      } else if(selected === '7_2') {
        dy_list_label.push('Research Publication - Conference Publication');
        dy_list_short_label.push('RPCP');
      } else if(selected === '7_3') {
        dy_list_label.push('Research Publication - Book and Book Chapters');
        dy_list_short_label.push('RPB');
      } else if(selected === '7_4') {
        dy_list_label.push('Patents');
        dy_list_short_label.push('PATENTS');
      } else if(selected === '1_2') {
        dy_list_label.push('Non-Teaching Staff');
        dy_list_short_label.push('NTS');
      } else if(selected === '1_1') {
        dy_list_label.push('Faculty Profile Details');
        dy_list_short_label.push(selected);
      }
  }
  const target = "Other";
  const paired = dy_list_label.map((item, i) => ({ item, value: dy_list_count[i] }));
  const others = paired.filter(p => p.item !== target);
  const targets = paired.filter(p => p.item === target);
  const sortedPairs = [...others, ...targets];

  const updated_labelList = sortedPairs.map(p => p.item);
  const updated_countList = sortedPairs.map(p => p.value);

  dataMap[selected] = updated_countList;
  label[selected] = updated_labelList;
  const backgroundColors = dy_list_short_label.map(item => categoryColors[item] || categoryColors['DEFAULT']);
  const borderColors = backgroundColors.map(color => color.replace('0.7', '1.0'));

  barChart.data.datasets[0].backgroundColor = backgroundColors;
  barChart.data.datasets[0].borderColor = borderColors;
  barChart.data.datasets[0].data = dataMap[selected];
//  barChart.data.datasets[0].label = dy_list_label[0];
  barChart.data.labels = label[selected];
  barChart.update();
});
