const form_type = JSON.parse(document.getElementById(`my-data-formtype`).textContent);

const data = JSON.parse(document.getElementById(`my-data-nts`).textContent);
const groupedData = data.reduce((acc, curr) => {
    acc[curr.email__email] = (acc[curr.email__email] || 0) + 1;
    return acc;
}, {});
const finalArray = Object.keys(groupedData).map(category_display => {
    return {
        category_display : category_display,
        count: groupedData[category_display]
    };
});
var totalSum = 0;
finalArray.forEach(email => {
    totalSum += email.count;
})

const data1 = JSON.parse(document.getElementById(`my-data-fdp1`).textContent);
const groupedData1 = data1.reduce((acc, curr) => {
    acc[curr.category_display] = (acc[curr.category_display] || 0) + 1;
    return acc;
}, {});
const finalArray1 = Object.keys(groupedData1).map(category_display => {
    return {
        category_display : category_display,
        count: groupedData1[category_display]
    };
});
var totalSum1 = 0;
finalArray1.forEach(cat => {
    totalSum1 += cat.count;
})

const data2 = JSON.parse(document.getElementById(`my-data-msc1`).textContent);
const groupedData2 = data2.reduce((acc, curr) => {
    acc[curr.category_display] = (acc[curr.category_display] || 0) + 1;
    return acc;
}, {});
const finalArray2 = Object.keys(groupedData2).map(category_display => {
    return {
        category_display : category_display,
        count: groupedData2[category_display]
    };
});
var totalSum2 = 0;
finalArray2.forEach(cat => {
    totalSum2 += cat.count;
})

const data3 = JSON.parse(document.getElementById(`my-data-eod1`).textContent);
const groupedData3 = data3.reduce((acc, curr) => {
    acc[curr.category_display] = (acc[curr.category_display] || 0) + 1;
    return acc;
}, {});
const finalArray3 = Object.keys(groupedData3).map(category_display => {
    return {
        category_display : category_display,
        count: groupedData3[category_display]
    };
});
var totalSum3 = 0;
finalArray3.forEach(cat => {
    totalSum3 += cat.count;
})

const data4 = JSON.parse(document.getElementById(`my-data-faa1`).textContent);
const groupedData4 = data4.reduce((acc, curr) => {
    acc[curr.category_display] = (acc[curr.category_display] || 0) + 1;
    return acc;
}, {});
const finalArray4 = Object.keys(groupedData4).map(category_display => {
    return {
        category_display : category_display,
        count: groupedData4[category_display]
    };
});
var totalSum4 = 0;
finalArray4.forEach(cat => {
    totalSum4 += cat.count;
})

const data5 = JSON.parse(document.getElementById(`my-data-sgc1`).textContent);
const groupedData5 = data5.reduce((acc, curr) => {
    acc[curr.category_display] = (acc[curr.category_display] || 0) + 1;
    return acc;
}, {});
const finalArray5 = Object.keys(groupedData5).map(category_display => {
    return {
        category_display : category_display,
        count: groupedData5[category_display]
    };
});
var totalSum5 = 0;
finalArray5.forEach(cat => {
    totalSum5 += cat.count;
})

const data6 = JSON.parse(document.getElementById(`my-data-rpj1`).textContent);
const groupedData6 = data6.reduce((acc, curr) => {
    acc[curr.noj] = (acc[curr.noj] || 0) + 1;
    return acc;
}, {});
const finalArray6 = Object.keys(groupedData6).map(category_display => {
    return {
        category_display : category_display,
        count: groupedData6[category_display]
    };
});
var totalSum6 = 0;
finalArray6.forEach(cat => {
    totalSum6 += cat.count;
})

const data7 = JSON.parse(document.getElementById(`my-data-rpcp1`).textContent);
const groupedData7 = data7.reduce((acc, curr) => {
    acc[curr.top] = (acc[curr.top] || 0) + 1;
    return acc;
}, {});
const finalArray7 = Object.keys(groupedData7).map(category_display => {
    return {
        category_display : category_display,
        count: groupedData7[category_display]
    };
});
var totalSum7 = 0;
finalArray7.forEach(cat => {
    totalSum7 += cat.count;
})

const data8 = JSON.parse(document.getElementById(`my-data-rpb1`).textContent);
const groupedData8 = data8.reduce((acc, curr) => {
    acc[curr.tob] = (acc[curr.tob] || 0) + 1;
    return acc;
}, {});
const finalArray8 = Object.keys(groupedData8).map(category_display => {
    return {
        category_display : category_display,
        count: groupedData8[category_display]
    };
});
var totalSum8 = 0;
finalArray8.forEach(cat => {
    totalSum8 += cat.count;
})

const data9 = JSON.parse(document.getElementById(`my-data-patents1`).textContent);
const groupedData9 = data9.reduce((acc, curr) => {
    acc[curr.top] = (acc[curr.top] || 0) + 1;
    return acc;
}, {});
const finalArray9 = Object.keys(groupedData9).map(category_display => {
    return {
        category_display : category_display,
        count: groupedData9[category_display]
    };
});
var totalSum9 = 0;
finalArray9.forEach(cat => {
    totalSum9 += cat.count;
})

const data10 = JSON.parse(document.getElementById(`my-data-mp1`).textContent);
const groupedData10 = data10.reduce((acc, curr) => {
    acc[curr.category_display] = (acc[curr.category_display] || 0) + 1;
    return acc;
}, {});
const finalArray10 = Object.keys(groupedData10).map(category_display => {
    return {
        category_display : category_display,
        count: groupedData10[category_display]
    };
});
var totalSum10 = 0;
finalArray10.forEach(cat => {
    totalSum10 += cat.count;
})

const data11 = JSON.parse(document.getElementById(`my-data-rp1`).textContent);
const groupedData11 = data11.reduce((acc, curr) => {
    acc[curr.category_display] = (acc[curr.category_display] || 0) + 1;
    return acc;
}, {});
const finalArray11 = Object.keys(groupedData11).map(category_display => {
    return {
        category_display : category_display,
        count: groupedData11[category_display]
    };
});
var totalSum11 = 0;
finalArray11.forEach(cat => {
    totalSum11 += cat.count;
})

const forms = [
    { form_number: "0", title: "Non-teaching Staff Profile Details", color: "#64748b", count: totalSum, innerCategory : finalArray, completeData: data },
    { form_number: "1", title: "Faculty Participation", color: "#22c55e", count: totalSum1, innerCategory : finalArray1, completeData: data1 },
    { form_number: "2", title: "MOOC's/Short Term Course/Course Completion", color: "#eab308" , count: totalSum2, innerCategory : finalArray2, completeData: data2 },
    { form_number: "3", title: "Events Organized by Department", color: "#ef4444" , count: totalSum3, innerCategory : finalArray3, completeData: data3 },
    { form_number: "4", title: "Faculty Awards and Achievements", color: "#06b6d4", count: totalSum4, innerCategory : finalArray4, completeData: data4 },
    { form_number: "5", title: "Sponsored Research/Grant Received/Consultancy", color: "#8b5cf6", count: totalSum5, innerCategory : finalArray5, completeData: data5 },
    { form_number: "6", title: "Research Publication - Journals", color: "#0ea5e9", count: totalSum6, innerCategory : finalArray6, completeData: data6 },
    { form_number: "7", title: "Research Publication - Conference Publication", color: "#3b82f6", count: totalSum7, innerCategory : finalArray7, completeData: data7 },
    { form_number: "8", title: "Research Publication - Book and Book Chapters", color: "#f59e0b", count: totalSum8, innerCategory : finalArray8, completeData: data8 },
    { form_number: "9", title: "Patents", color: "#14b8a6",count: totalSum9, innerCategory : finalArray9, completeData: data9 },
    { form_number: "10", title: "M.Tech/Ph.D Guided", color: "#06b6d4", count: totalSum10, innerCategory : finalArray10, completeData: data10 },
    { form_number: "11", title: "Resource Person", color: "#ec4899", count: totalSum11, innerCategory : finalArray11, completeData: data11 }
];
document.getElementById("app").innerHTML = forms.map(f => {
    if(form_type === "filled_forms" && f.count > 0) {
        return  `<div class="primary-card" style="--card-color:${f.color}">
                <div class="primary-header">
                    <div>
                        <h5>${f.title}</h5>
                        <small>${f.count} Forms Filled</small>
                    </div>
                    <i class="fas fa-chevron-down rotate"></i>
                </div>

                <div class="primary-body">
                    <div class="inner-content">
                        ${f.innerCategory.map(s => {
                            if (s.count > 0) {
                            return `    <div class="sub-row">
                                    <div class="sub-header">
                                        <span>${s.category_display}</span>
                                        <div class = "w-12 h-12 bg-indigo-100 rounded-full flex items-center justify-center">${s.count}</div>
                                    </div>

                                    <div class="entry-wrapper">
                                        <div>
                                            <div class="entry-padding">
                                                ${f.completeData.map(data => {
                                                    const id = data.id;
                                                    const catMatch = data.category_display || data.email__email || data.noj || data.top || data.tob || data.top;
                                                    const value = Object.values(data)[1];
                                                    if(catMatch === s.category_display) {
                                                        return `
                                                            <div class="entry-item d-flex ms-auto justify-content-between align-items-center" style="padding: 8px 0; border-bottom: 1px solid #eee;">
                                                                <div style="flex: 1;" class="ms-3">${value}</div>
                                                                <div style="margin-left: 10px;">
                                                                    <a href="progressdetails/${f.form_number}/${id}" style="text-decoration: none; color: #007bff;">
                                                                        <span class="px-3 py-1 bg-green-100 text-green-700 rounded-full text-sm font-semibold"><button type="button" class="btn btn-sm btn-outline-success"><i class="fas fa-pencil-alt"></i> <b>Edit </b> </button></span> 
                                                                    </a>
                                                                </div>
                                                            </div>
                                                        `;
                                                    }
                                                }).join("")}
                                            </div>
                                        </div>
                                    </div>
                                </div> 
                            `;} else {
                                return `
                                `;
                            }
                        }).join("")}
                    </div>
                </div>
            </div>
            `;
        } else if(form_type == "unfilled_forms") {
            if (f.count == 0)  {
                return  `
                    <div class="primary-card" style="--card-color:${f.color}">
                        <div class="primary-header">
                            <div>
                                <h5>${f.title}</h5>
                                <small>${f.count} Forms Filled</small>
                            </div>
                            <i class="fas fa-chevron-down rotate"></i>
                        </div>

                        <div class="primary-body">
                            <div class="inner-content">
                                ${f.innerCategory.map(s => {
                                    if (s.count == 0) { 
                                        return  `<div class="sub-row">
                                                    <div class="sub-header">
                                                        <span>${s.category_display}</span>
                                                        <div class = "w-12 h-12 bg-indigo-100 rounded-full flex items-center justify-center">${s.count}</div>
                                                    </div>
                                                </div>
                                        `;
                                    }
                                }).join("")}
                            </div>
                        </div>
                    </div>
                `;
            }
        }
    }
).join("");

/* EVENTS */
document.querySelectorAll(".primary-header").forEach(h => {
    h.onclick = () => {
        document.querySelectorAll(".primary-card").forEach(c => {
            if (c !== h.parentElement) c.classList.remove("open");
        });
        h.parentElement.classList.toggle("open");
    };
});

document.querySelectorAll(".sub-header").forEach(h => {
    h.onclick = e => {
        e.stopPropagation();
        const row = h.parentElement;
        row.classList.toggle("open");
    };
});