const checkboxGroup = document.getElementById('checkboxGroup');
const inputFields = document.getElementById('inputFields');
const subFormsContainer = document.getElementById('subFormsContainer');
const inputCount = document.getElementById('inputCount');
const subformCount = document.getElementById('subformCount');

const quantities = {};
const form_number = window.location.href.substring(window.location.href.lastIndexOf('/') + 1)

const fieldInfo = {
    'Organizer': 'for e.g : SKIT, M&G, Jaipur',
    'SKIT Approved': 'Grant received from SKIT (Yes/No)',
    'Sponsered By': "Write 'NA' if non sponsored",
    'Session': 'A Session e.g 2024-25 starts at July 2024 and ends at June 2025',
    'Proof Enclosed': 'Certificate/Proof is to be uploaded to the right of this field.',
    'Upload Certificate/Proof': 'Rename file as:  session_FullName_TypeofEvent_No._Title e.g 2024-25_AjaySharma_FDP_1_GenerativeAI',
    'Timeline of Course': 'e.g.: Jan-April 2024',
    'Name of the Course': 'Please fill complete name of the course that is mentioned in your certificate',
    'Offering Agency / Organizer': 'Swayam/Nptel/Infosys Springboard/Coursera/edx/Udemy etc.',
    'Upload Certificate(MOOC)': "Only upload course completed certificate.  Rename file as &quot;Course name_Faculty Name_year of completion e.g DBMS_Dr Anjana_2024&quot;. Please don't upload FDP certificate for the same",
    'Title of the Professional Development Program Organized': "e.g : Expert Lecture on 'Building the Perfect Conference Proposal: A Comprehensive Approach', ATAL Sponsored Advanced FDP on 'Exploring Advanced AI and Data Science Applications in Healthcare'",
    'Academic Department/ Cell / Committees/ Labs /COE' : 'e.g : CSE/COE, ECE',
    'Collaboration Details': 'e.g : Spoken Tutorial IIT Bombay. Write NA if not applicable',
    'Grant Details': 'e.g : Rs 350000 from AICTE ATAL.',
    'Association with professional societies for organization of event': 'e.g IEEE Computer Society Chapter, IEEE Delhi Section. Write NA if not applicable',
    'Not Applicable': 'Write NA if not applicable',
    'Event report attached in proper format': 'Merge One Page Report and Detailed Report in a single file to be uploaded at the end of this form.',
    'Upload Event Report': 'Merge One Page Report and Detailed Report in a single file.Rename file as: session_event-type_title e.g : 2024-25_expert_lecture_report_GenereativeAI',
    'Name of the Award/Achievement': "Please fill complete name of award/achievement like 'Silver Medal in course - Computer Networks and Internet Protocol'  or  'Young Scientist Award in Research'.  For research only include best paper award or any other award in research, please don't add paper presented/published details here",
    'Position / Award For': '(First/Second/Topper...) or Award for (Title)(E.g. Gold Medal, best teacher award, Topper 1% ,top performing mentor etc.,)',
    'Agency / Organization': 'Infosys/NPTEL/AICTE  etc.',
    'Prize': 'Cash amount /certificate/ any other',
    'Upload Award Certificate/Proof': 'Rename file as : session_Facultyname_awardname for e.g : 2024-25_AjaySharma_TopPerformingMentor',
    'Remark': 'Please fill it if you have any extra information regarding above',
    'Name of the Funding Agency': '(MSME/DST/CSIR/SERB /Industry etc.)',
    'Upload Proof': 'rename file as 2024-25_AnujSharma_Grant',
    'DOI': 'Paste full link for e.g: https://doi.org/10.1109/ACCESS.2023.3321861',
    'Link to website of the Journal': 'Paste full link for e.g: https://www.tarupublications.com/journal/JIOS',
    'Link to article/paper/abstract of the article': '(Direct link to the webpage where the abstract of paper is displayed) Paste full link for  e.g : https://ieeexplore.ieee.org/stamp/stamp.jsp?arnumber=10271389',
    'Affiliating Institute at the time of publication': 'Write full name for e.g: Swami Keshvanand Institute of Technology, Management & Gramothan (SKIT), Jaipur',
    'Is SKIT student associated?': 'Is SKIT student author/co-author?',
    'If Yes , Write student(s) details (Program, Branch, RollNo/EnrollNo, Name)': 'e.g : B.Tech, CSE(AI), 22ESKCA837, Amit Verma. If No write NA',
    'Upload Full Paper': 'rename file as session_author-name for e.g: 2024-25_AjaySharma',
    'Title of the Conference': 'for e.g : International Conference on Information Management & Machine Intelligence',
    'Title of the proceedings of the conference': 'for e.g: Proceedings of the International Conference on Intelligent Computing, Communication and Information Security ICICCIS 2022',
    'Is the Patent granted ?': "Select 'Yes' if the Patent is both published and granted , and 'No' if the Patent is only published, but not yet granted.",
    'Is SKIT student associated?(Patent)': 'Is SKIT student associated with the Patent (Is SKIT student inventor/applicant/owner etc)?',
    'Title of Event/ Exam Name': 'for e.g. : University Practical Exam B.Tech CSE V Sem  2023-24, International Conference on AI Systems and Sustainable Technologies 2025, Name of the Journal if editorial board member etc.',
    'Subject Area/Subject Name/Lab Name/Session Name': 'for e.g: Object Oriented Programming Lab, Name of session',
    'Proof (Certificate/Mail)': 'Any proof in (certificate/mail screenshot/document/etc) which validates you as a resource person'
};

const categoryValue = {
    'FDP': 'FDP',
    'Workshop': 'WKP',
    'Conference': 'CON',
    'STTP': 'STTP',
    'Seminar': 'SEM',
    'Lecture Series': 'LS',
    'Symposium': 'SYM',
    'External  Examination(UG)': 'EE(UG)',
    'External  Examination(PG)': 'EE(PG)',
    'Journal': 'JOU',
    'Expert Lecture': 'EL',
    'Expert Talk': 'ET',
    'Hackathon': 'HAT',
    'Training': 'TRA',
    'Internship': 'INT',
    'BOS': 'BOS',
    'DRC': 'DRC',
    'Short Term Courses': 'STC',
    'MOOC courses': 'MOOC',
    'Induction Program': 'IP',
    'Education': 'EDU',
    'Research': 'REA',
    'Sports': 'SPO',
    'Sponsored Grant': 'SG',
    'Research Project': 'RP',
    'Consultancy': 'CONS',
    'M.Tech Students': 'M_TECH',
    'Ph.D Students': 'PH_D',
    'Other' : 'OTH'
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            let cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const csrfToken = getCookie('csrftoken');

checkboxGroup.addEventListener('change', (e) => {
    if (e.target.type === 'checkbox') {
        generateInputFields();
    }
});




function generateInputFields() {
    const checkedBoxes = Array.from(checkboxGroup.querySelectorAll('input[type="checkbox"]:checked'));
    inputFields.innerHTML = '';

    if (checkedBoxes.length === 0) {
        inputFields.innerHTML = '<div class="empty-state">Select checkboxes above to generate input fields</div>';
        inputCount.textContent = '0 fields';
        generateSubForms();
        return;
    }

    inputCount.textContent = `${checkedBoxes.length} field${checkedBoxes.length !== 1 ? 's' : ''}`;



    checkedBoxes.forEach(checkbox => {
        const value = checkbox.value;
        const inputGroup = document.createElement('div');
        inputGroup.className = 'input-group';
        inputGroup.style = 'flex-direction: column; height: 76px';


        inputGroup.innerHTML = `
            <div class = "d-flex m-2">
            <label for="input-${value}" class = "form-label mt-1"><b>How many ${value}?</b></label>
            <div class = "col-4 ms-3">
            <input
                type="number"
                class = "form-control"
                id="input-${value}"
                min="0"
                max="20"
                placeholder="Enter quantity (max 20)"
                value="${quantities[value] || ''}"
            >
            </div>
            </div>
        `;

        inputFields.appendChild(inputGroup);

        const input = inputGroup.querySelector('input');
        input.addEventListener('input', (e) => {
            let val = parseInt(e.target.value) || 0;
            if (val > 20) val = 20;
            if (val < 0) val = 0;
            e.target.value = val || '';
            quantities[value] = val;
            generateSubForms();
        });
    });
}

function generateSubForms() {
    subFormsContainer.innerHTML = '';
    let totalForms = 0;

    const checkedBoxes = Array.from(checkboxGroup.querySelectorAll('input[type="checkbox"]:checked'));

    if (checkedBoxes.length === 0) {
        subFormsContainer.innerHTML = '<div class="empty-state">Enter quantities above to generate sub-forms</div>';
        subformCount.textContent = '0 forms';
        return;
    }

    let hasQuantity = false;

    checkedBoxes.forEach(checkbox => {
        const category = checkbox.value;
        const quantity = quantities[category] || 0;

        if (quantity > 0) {
            hasQuantity = true;
            for (let i = 1; i <= quantity; i++) {
                totalForms++;

                const subForm = document.createElement('form');
                subForm.className = 'sub-form';
                subForm.style = 'flex-direction: column';
                subForm.method  = 'POST';
                subForm.action = '/save_all_forms/' + form_number;
                subForm.enctype = 'multipart/form-data'
                if(form_number == '1') {
                    subForm.innerHTML = `
                        <div class="sub-form-title" style = "font-size: 1.5rem; color: #667eea;"><b>${category} #${i}</b></div>
                        <input type = "hidden" name = "category" value = "${categoryValue[category]}">
                        <input type = "hidden" name = "csrfmiddlewaretoken" value = "${csrfToken}">
                        <div class="sub-form-fields">
                            <div class="row g-3">
                                <div class="col-md-4">
                                    <div class="row align-items-center">
                                        <label for="top" class="col-sm-4 col-form-label">Title Of Program<span class="ms-1" style="color: red;">*</span></label>
                                        <div class = "col-md-8">
                                            <input type="text" class="form-control custom-back" id="top" placeholder="Enter title of the program" name="top" required>
                                        </div>
                                    </div>
                                </div>
                                <div class="col-md-4">
                                    <div class="row align-items-center">
                                        <label class="col-sm-4 col-form-label">Mode<span class="ms-1" style="color: red;">*</span></label>
                                        <div class = "col-sm-8">
                                            <div class="d-flex column-gap-4">
                                                <div class="form-check">
                                                    <input type="radio" class="form-check-input" id="radio1" name="optradio" value="On" required>
                                                    <label class="form-check-label" for="radio1">Online</label>
                                                </div>
                                                <div class="form-check">
                                                    <input type="radio" class="form-check-input" id="radio2" name="optradio" value="Of">
                                                    <label class="form-check-label" for="radio2">Offline</label>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                                <div class="col-md-4">
                                    <div class="row align-items-center">
                                        <label class="col-sm-4 col-form-label">Level<span class="ms-1" style="color: red;">*</span></label>
                                        <div class="col-sm-8">
                                            <div class="d-flex column-gap-4">
                                                <div class="form-check">
                                                    <input type="radio" class="form-check-input" id="radio3" name="optradio1" value="Na" required>
                                                    <label class="form-check-label" for="radio3">National</label>
                                                </div>
                                                <div class="form-check">
                                                    <input type="radio" class="form-check-input" id="radio4" name="optradio1" value="In">
                                                    <label class="form-check-label" for="radio4">International</label>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                                <div class="col-md-4">
                                    <div class="row align-items-center">
                                        <label class="col-sm-4 col-form-label">Organizer<span class="ms-1" style="color: red;">*</span><span class="fa-solid fa-circle-info" data-bs-toggle="tooltip" data-bs-placement="top" title="${fieldInfo['Organizer']}"></span></label>
                                        <div class="col-sm-8">
                                            <input type="text" class="form-control" placeholder="Enter organizer" name = "organizer" required>
                                        </div>
                                    </div>
                                </div>
                                <div class="col-md-4">
                                    <div class="row align-items-center">
                                        <label class="col-sm-4 col-form-label">Sponsored By<span class="ms-1" style="color: red;">*</span><span class="fa-solid fa-circle-info" data-bs-toggle="tooltip" data-bs-placement="top" title="${fieldInfo['Sponsered By']}"></span></label>
                                        <div class="col-sm-8">
                                            <input type="text" class="form-control" placeholder="Enter sponsors" name = "sponser" required>
                                        </div>
                                    </div>
                                </div>
                                <div class="col-md-4">
                                    <div class="row align-items-center">
                                        <label class="col-sm-4 col-form-label">SKIT Approved<span class="ms-1" style="color: red;">*</span><span class="fa-solid fa-circle-info" data-bs-toggle="tooltip" data-bs-placement="top" title="${fieldInfo['SKIT Approved']}"></span></label>
                                        <div class="col-sm-8">
                                            <div class="d-flex column-gap-4">
                                                <div class="form-check">
                                                    <input type="radio" class="form-check-input" id="radio5" name="optradio2" value="y" required>
                                                    <label class="form-check-label" for="radio5">Yes</label>
                                                </div>
                                                <div class="form-check">
                                                    <input type="radio" class="form-check-input" id="radio6" name="optradio2" value="N">
                                                    <label class="form-check-label" for="radio6">No</label>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                                <div class="col-md-4">
                                    <div class="row align-items-center">
                                        <label class="col-sm-4 col-form-label">From Date<span class="ms-1" style="color: red;">*</span></label>
                                        <div class="col-sm-8">
                                            <input type="date" class="form-control" name = "begi_date" required>
                                        </div>
                                    </div>
                                </div>
                                <div class="col-md-4">
                                    <div class="row align-items-center">
                                        <label class="col-sm-4 col-form-label">To Date<span class="ms-1" style="color: red;">*</span></label>
                                        <div class="col-sm-8">
                                            <input type="date" class="form-control" name = "end_date" required>
                                        </div>
                                    </div>
                                </div>
                                <div class="col-md-4">
                                    <div class="row align-items-center">
                                        <label class="col-sm-4 col-form-label">Session<span class="ms-1" style="color: red;">*</span><span class="fa-solid fa-circle-info" data-bs-toggle="tooltip" data-bs-placement="top" title="${fieldInfo['Session']}"></span></label>
                                        <div class="col-sm-8">
                                            <select class="form-control custom-back-select" name="sessionyear" id="sessionyear" required>
                                                <option value="" selected disabled>Select your Session</option>
                                                <option value="2025-26">2025-26</option>
                                                <option value="2026-27">2026-27</option>
                                                <option value="2027-28">2027-28</option>
                                                <option value="2028-29">2028-29</option>
                                                <option value="2029-30">2029-30</option>
                                            </select>
                                        </div>
                                    </div>
                                </div>
                                <div class="col-md-4">
                                    <div class="row align-items-center">
                                        <label class="col-sm-4 col-form-label">No. of days<span class="ms-1" style="color: red;">*</span></label>
                                        <div class="col-sm-8">
                                            <input type="number" class="form-control" placeholder="Enter number of days" name = "num_of_days" required>
                                        </div>
                                    </div>
                                </div>
                                <div class="col-md-4">
                                    <div class="row align-items-center">
                                        <label class="col-sm-4 col-form-label">Proof Enclosed<span class="ms-1" style="color: red;">*</span><span class="fa-solid fa-circle-info" data-bs-toggle="tooltip" data-bs-placement="top" title="${fieldInfo['Proof Enclosed']}"></span></label>
                                        <div class="col-sm-8">
                                            <div class="d-flex column-gap-4">
                                                <div class="form-check">
                                                    <input type="radio" class="form-check-input" id="radio5" name="optradio3" value="y" required>
                                                    <label class="form-check-label" for="radio5">Yes</label>
                                                </div>
                                                <div class="form-check">
                                                    <input type="radio" class="form-check-input" id="radio6" name="optradio3" value="N">
                                                    <label class="form-check-label" for="radio6">No</label>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                                <div class="col-md-6">
                                    <div class="row align-items-center">
                                        <label class="col-sm-4 col-form-label">Upload Certificate/Proof(Only PDF)<span class="ms-1" style="color: red;">*</span><span class="fa-solid fa-circle-info" data-bs-toggle="tooltip" data-bs-placement="top" title="${fieldInfo['Upload Certificate/Proof']}"></span></label>
                                        <div class="col-sm-6">
                                            <input type="file" class="form-control" placeholder="Upload files" accept=".pdf" name="proof_file" required>
                                        </div>
                                    </div>
                                </div>
                                <div class="col-md-2 mt-5">
                                    <div class="row align-items-center">
                                        <div class="col-sm-8">
                                            <button type = "button" class="btn btn-primary"><i class="fa-solid fa-eye"></i>View</button>
                                        </div>
                                    </div>
                                </div>
                                <div class = "col-md-12">
                                    <div class="row align-items-center justify-content-center">
                                        <button type = "submit" class="btn btn-primary rounded-pill" style = "width: 10%;">Submit</button>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <hr>
                    `;
                } else if(form_number == '2') {
                    subForm.innerHTML = `
                        <div class="sub-form-title" style = "font-size: 1.5rem; color: #667eea;"><b>${category} #${i}</b></div>
                        <input type = "hidden" name = "csrfmiddlewaretoken" value = "${csrfToken}">
                        <div class="sub-form-fields">
                            <div class="row g-3">
                                <div class="col-md-6">
                                    <div class="row align-items-center">
                                        <label for="top" class="col-sm-4 col-form-label">Timeline of course<span class="ms-1" style="color: red;">*</span><span class="fa-solid fa-circle-info" data-bs-toggle="tooltip" data-bs-placement="top" title="${fieldInfo['Timeline of Course']}"></span></label>
                                        <div class = "col-md-8">
                                            <input type="text" class="form-control" id="toc" placeholder="Enter timeline of the program" name="toc" required>
                                        </div>
                                    </div>
                                </div>
                                <div class="col-md-6">
                                    <div class="row align-items-center">
                                        <label class="col-sm-4 col-form-label">Name of the Course<span class="ms-1" style="color: red;">*</span><span class="fa-solid fa-circle-info" data-bs-toggle="tooltip" data-bs-placement="top" title="${fieldInfo['Name of the Course']}"></span></label>
                                        <div class="col-sm-8">
                                            <input type="text" class="form-control" placeholder="Enter name of course" name = "noc" required>
                                        </div>
                                    </div>
                                </div>
                                <div class="col-md-6">
                                    <div class="row align-items-center">
                                        <label class="col-sm-4 col-form-label">Duration of Course<span class="ms-1" style="color: red;">*</span></label>
                                        <div class = "col-sm-8">
                                            <div class="d-flex column-gap-4">
                                                <div class="form-check">
                                                    <input type="radio" class="form-check-input" id="radio1" name="optradio3" value="4" required>
                                                    <label class="form-check-label" for="radio1">4 Week</label>
                                                </div>
                                                <div class="form-check">
                                                    <input type="radio" class="form-check-input" id="radio2" name="optradio3" value="8">
                                                    <label class="form-check-label" for="radio2">8 Week</label>
                                                </div>
                                                <div class="form-check">
                                                    <input type="radio" class="form-check-input" id="radio3" name="optradio3" value="12">
                                                    <label class="form-check-label" for="radio2">12 Week</label>
                                                </div>
                                                <div class="form-check">
                                                    <input type="radio" class="form-check-input" id="radio4" name="optradio3" value="O">
                                                    <label class="form-check-label" for="radio2">Other</label>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                                <div class="col-md-6">
                                    <div class="row align-items-center">
                                        <label class="col-sm-4 col-form-label">Start Date of Course<span class="ms-1" style="color: red;">*</span></label>
                                        <div class="col-sm-8">
                                            <input type="date" class="form-control" name = "begi_date" required>
                                        </div>
                                    </div>
                                </div>
                                <div class="col-md-6">
                                    <div class="row align-items-center">
                                        <label class="col-sm-4 col-form-label">End Date of Course<span class="ms-1" style="color: red;">*</span></label>
                                        <div class="col-sm-8">
                                            <input type="date" class="form-control" name = "end_date" required>
                                        </div>
                                    </div>
                                </div>
                                <div class="col-md-6">
                                    <div class="row align-items-center">
                                        <label class="col-sm-4 col-form-label">Offering Agency/ Organizer<span class="ms-1" style="color: red;">*</span><span class="fa-solid fa-circle-info" data-bs-toggle="tooltip" data-bs-placement="top" title="${fieldInfo['Offering Agency / Organizer']}"></span></label>
                                        <div class="col-sm-8">
                                            <input type="text" class="form-control" placeholder="Enter Offering Agency" name = "ofo" required>
                                        </div>
                                    </div>
                                </div>
                                <div class="col-md-12">
                                    <div class="row align-items-center">
                                        <label class="col-sm-4 col-form-label">Certificate Type<span class="ms-1" style="color: red;">*</span></label>
                                        <div class="col-sm-8">
                                            <div class="d-flex column-gap-4">
                                                <div class="form-check">
                                                    <input type="radio" class="form-check-input" id="radio5" name="optradio1" value="G" required>
                                                    <label class="form-check-label" for="radio5">Gold</label>
                                                </div>
                                                <div class="form-check">
                                                    <input type="radio" class="form-check-input" id="radio6" name="optradio1" value="S">
                                                    <label class="form-check-label" for="radio6">Silver</label>
                                                </div>
                                                <div class="form-check">
                                                    <input type="radio" class="form-check-input" id="radio7" name="optradio1" value="E">
                                                    <label class="form-check-label" for="radio7">Elite</label>
                                                </div>
                                                <div class="form-check">
                                                    <input type="radio" class="form-check-input" id="radio8" name="optradio1" value="SC">
                                                    <label class="form-check-label" for="radio8">Successfully Completed</label>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                                <div class="col-md-12">
                                    <div class="row align-items-center">
                                        <label class="col-sm-4 col-form-label">Any category from below<span class="ms-1" style="color: red;">*</span></label>
                                        <div class="col-sm-8">
                                            <div class="d-flex column-gap-4">
                                                <div class="form-check">
                                                    <input type="radio" class="form-check-input" id="radio9" name="optradio2" value="1" required>
                                                    <label class="form-check-label" for="radio9">Topper of 1% in this course</label>
                                                </div>
                                                <div class="form-check">
                                                    <input type="radio" class="form-check-input" id="radio10" name="optradio2" value="2">
                                                    <label class="form-check-label" for="radio10">Topper of 2% in this course</label>
                                                </div>
                                                <div class="form-check">
                                                    <input type="radio" class="form-check-input" id="radio11" name="optradio2" value="5">
                                                    <label class="form-check-label" for="radio11">Topper of 5% in this course</label>
                                                </div>
                                                <div class="form-check">
                                                    <input type="radio" class="form-check-input" id="radio12" name="optradio2" value="10">
                                                    <label class="form-check-label" for="radio12">Topper of 10% in this course</label>
                                                </div>
                                                <div class="form-check">
                                                    <input type="radio" class="form-check-input" id="radio13" name="optradio2" value="NA">
                                                    <label class="form-check-label" for="radio13">Not Applicable</label>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                                <div class="col-md-6">
                                    <div class="row align-items-center">
                                        <label class="col-sm-4 col-form-label">Session<span class="ms-1" style="color: red;">*</span><span class="fa-solid fa-circle-info" data-bs-toggle="tooltip" data-bs-placement="top" title="${fieldInfo['Session']}"></span></label>
                                        <div class="col-sm-8">
                                            <select class="form-control custom-back-select" name="sessionyear" id="sessionyear" required>
                                                <option value="" selected disabled>Select your Session</option>
                                                <option value="2025-26">2025-26</option>
                                                <option value="2026-27">2026-27</option>
                                                <option value="2027-28">2027-28</option>
                                                <option value="2028-29">2028-29</option>
                                                <option value="2029-30">2029-30</option>
                                            </select>
                                        </div>
                                    </div>
                                </div>
                                <div class="col-md-6">
                                    <div class="row align-items-center">
                                        <label class="col-sm-4 col-form-label">Remarks(If any)</label>
                                        <div class="col-sm-8">
                                            <input type="text" class="form-control" placeholder="Enter Remarks" name = "remarks">
                                        </div>
                                    </div>
                                </div>
                                <div class="col-md-6">
                                    <div class="row align-items-center">
                                        <label class="col-sm-4 col-form-label">Upload Certificate/Proof(Only PDF)<span class="ms-1" style="color: red;">*</span><span class="fa-solid fa-circle-info" data-bs-toggle="tooltip" data-bs-placement="top" title="${fieldInfo['Upload Certificate(MOOC)']}"></span></label>
                                        <div class="col-sm-6">
                                            <input type="file" class="form-control" placeholder="Upload files" accept=".pdf" name="proof_file" required>
                                        </div>
                                    </div>
                                </div>
                                <div class="col-md-2 mt-5">
                                    <div class="row align-items-center">
                                        <div class="col-sm-8">
                                            <button type = "button" class="btn btn-primary"><i class="fa-solid fa-eye"></i>View</button>
                                        </div>
                                    </div>
                                </div>
                                <div class = "col-md-12">
                                    <div class="row align-items-center justify-content-center">
                                        <button type = "submit" class="btn btn-primary rounded-pill" style = "width: 10%;">Submit</button>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <hr>
                    `;
                } else if (form_number == 3) {
                    subForm.innerHTML = `
                        <div class="sub-form-title" style = "font-size: 1.5rem; color: #667eea;"><b>${category} #${i}</b></div>
                        <input type = "hidden" name = "csrfmiddlewaretoken" value = "${csrfToken}">
                        <input type = "hidden" name = "category" value = "${categoryValue[category]}">
                        <div class="sub-form-fields">
                            <div class="row g-3">
                                <div class="col-md-6">
                                    <div class="row align-items-center">
                                        <label class="col-sm-4 col-form-label">Event organized for<span class="ms-1" style="color: red;">*</span></label>
                                        <div class="col-sm-8 mt-4">
                                            <div class="d-flex column-gap-4">
                                                <div class="form-check">
                                                    <input type="checkbox" class="form-check-input group-required" id="radio1" name="optradio3" value="S">
                                                    <label class="form-check-label" for="radio1">Students</label>
                                                </div>
                                                <div class="form-check">
                                                    <input type="checkbox" class="form-check-input" id="radio2" name="optradio3" value="TS">
                                                    <label class="form-check-label" for="radio2">Teaching Staff</label>
                                                </div>
                                                <div class="form-check">
                                                    <input type="checkbox" class="form-check-input" id="radio3" name="optradio3" value="NTS">
                                                    <label class="form-check-label" for="radio3">Non-Teaching Staff</label>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                                <div class="col-md-6">
                                    <div class="row align-items-center">
                                        <label class="col-sm-4 col-form-label">Title of the Professional Development Program Organized<span class="ms-1" style="color: red;">*</span><span class="fa-solid fa-circle-info" data-bs-toggle="tooltip" data-bs-placement="top" title="${fieldInfo['Title of the Professional Development Program Organized']}"></span></label>
                                        <div class = "col-sm-8">
                                            <input type="text" class="form-control" placeholder="Enter title of the Professional Development Program Organized" name = "topdpo" required>
                                        </div>
                                    </div>
                                </div>
                                <div class="col-md-6" style = "margin-top: 4rem;">
                                    <div class="row align-items-center">
                                        <label class="col-sm-4 col-form-label">No. of participants<span class="ms-1" style="color: red;">*</span></label>
                                        <div class = "col-sm-8">
                                            <input type="number" class="form-control" placeholder="Enter no. of participants" name = "nop" required>
                                        </div>
                                    </div>
                                </div>
                                <div class="col-md-6">
                                    <div class="row align-items-center">
                                        <label class="col-sm-4 col-form-label">Academic Department/ Cell/ Committees/ Labs/ COE<span class="ms-1" style="color: red;">*</span><span class="fa-solid fa-circle-info" data-bs-toggle="tooltip" data-bs-placement="top" title="${fieldInfo['Academic Department/ Cell / Committees/ Labs /COE']}"></span></label>
                                        <div class = "col-sm-8">
                                            <input type="text" class="form-control" placeholder="Enter Academic Department/ Cell/ Committees/ Labs/ COE" name = "adcc" required>
                                        </div>
                                    </div>
                                </div>
                                <div class="col-md-6 mt-5">
                                    <div class="row align-items-center">
                                        <label class="col-sm-4 col-form-label">Academic Session<span class="ms-1" style="color: red;">*</span><span class="fa-solid fa-circle-info" data-bs-toggle="tooltip" data-bs-placement="top" title="${fieldInfo['Session']}"></span></label>
                                        <div class="col-sm-8">
                                            <select class="form-control custom-back-select" name="sessionyear" id="sessionyear" required>
                                                <option value="" selected disabled>Select your Session</option>
                                                <option value="2025-26">2025-26</option>
                                                <option value="2026-27">2026-27</option>
                                                <option value="2027-28">2027-28</option>
                                                <option value="2028-29">2028-29</option>
                                                <option value="2029-30">2029-30</option>
                                            </select>
                                        </div>
                                    </div>
                                </div>
                                <div class="col-md-6">
                                    <div class="row align-items-center">
                                        <label class="col-sm-4 col-form-label">Certificate Type<span class="ms-1" style="color: red;">*</span></label>
                                        <div class="col-sm-8">
                                            <div class="d-flex column-gap-4">
                                                <div class="form-check">
                                                    <input type="radio" class="form-check-input" id="radio3" name="optradio1" value="S" required>
                                                    <label class="form-check-label" for="radio3">Sponsored</label>
                                                </div>
                                                <div class="form-check">
                                                    <input type="radio" class="form-check-input" id="radio4" name="optradio1" value="NS">
                                                    <label class="form-check-label" for="radio4">Non-Sponsored</label>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                                <div class="col-md-6">
                                    <div class="row align-items-center">
                                        <label class="col-sm-4 col-form-label">Name of Sponsoring Agency(if Sponsored)<span class="ms-1" style="color: red;">*</span><span class="fa-solid fa-circle-info" data-bs-toggle="tooltip" data-bs-placement="top" title="${fieldInfo['Not Applicable']}"></span></label>
                                        <div class = "col-sm-8">
                                            <input type="text" class="form-control" placeholder="Enter name of sponsoring agency" name = "nosa" required>
                                        </div>
                                    </div>
                                </div>
                                <div class="col-md-6">
                                    <div class="row align-items-center">
                                        <label class="col-sm-4 col-form-label">Collaboration Details<span class="ms-1" style="color: red;">*</span><span class="fa-solid fa-circle-info" data-bs-toggle="tooltip" data-bs-placement="top" title="${fieldInfo['Collaboration Details']}"></span></label>
                                        <div class = "col-sm-8">
                                            <input type="text" class="form-control" placeholder="Enter collaboration details" name = "cd" required>
                                        </div>
                                    </div>
                                </div>
                                <div class="col-md-6">
                                    <div class="row align-items-center">
                                        <label class="col-sm-4 col-form-label">Start Date of the Event<span class="ms-1" style="color: red;">*</span></label>
                                        <div class="col-sm-8">
                                            <input type="date" class="form-control" name = "begi_date" required>
                                        </div>
                                    </div>
                                </div>
                                <div class="col-md-6">
                                    <div class="row align-items-center">
                                        <label class="col-sm-4 col-form-label">End Date of the Event<span class="ms-1" style="color: red;">*</span></label>
                                        <div class="col-sm-8">
                                            <input type="date" class="form-control" name = "end_date" required>
                                        </div>
                                    </div>
                                </div>
                                <div class="col-md-6">
                                    <div class="row align-items-center">
                                        <label class="col-sm-4 col-form-label">Grant Received(YES/NO)<span class="ms-1" style="color: red;">*</span><span class="fa-solid fa-circle-info" data-bs-toggle="tooltip" data-bs-placement="top" title="${fieldInfo['SKIT Approved']}"></span></label>
                                        <div class="col-sm-8">
                                            <div class="d-flex column-gap-4">
                                                <div class="form-check">
                                                    <input type="radio" class="form-check-input" id="radio5" name="optradio2" value="y" required>
                                                    <label class="form-check-label" for="radio5">Yes</label>
                                                </div>
                                                <div class="form-check">
                                                    <input type="radio" class="form-check-input" id="radio6" name="optradio2" value="N">
                                                    <label class="form-check-label" for="radio6">No</label>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                                <div class="col-md-6">
                                    <div class="row align-items-center">
                                        <label class="col-sm-4 col-form-label">Grant Details<span class="ms-1" style="color: red;">*</span><span class="fa-solid fa-circle-info" data-bs-toggle="tooltip" data-bs-placement="top" title="${fieldInfo['Grant Details']}"></label>
                                        <div class = "col-sm-8">
                                            <input type="text" class="form-control" placeholder="Enter grant details" name = "gd" required>
                                        </div>
                                    </div>
                                </div>
                                <div class="col-md-6">
                                    <div class="row align-items-center">
                                        <label class="col-sm-4 col-form-label">Association with professional societies for organization of event<span class="ms-1" style="color: red;">*</span><span class="fa-solid fa-circle-info" data-bs-toggle="tooltip" data-bs-placement="top" title="${fieldInfo['Association with professional societies for organization of event']}"></span></label>
                                        <div class="col-sm-8">
                                            <input type="text" class="form-control" placeholder="Enter details" name = "awpsfooe" required>
                                        </div>
                                    </div>
                                </div>
                                <div class="col-md-6">
                                    <div class="row align-items-center">
                                        <label class="col-sm-4 col-form-label">Number of SKIT students participated (Provide list of students with their RTU roll no. & Certificates)<span class="ms-1" style="color: red;">*</span><span class="fa-solid fa-circle-info" data-bs-toggle="tooltip" data-bs-placement="top" title="${fieldInfo['Not Applicable']}"></span></label>
                                        <div class="col-sm-8">
                                            <input type="number" class="form-control" placeholder="Enter details" name = "nossp" required>
                                        </div>
                                    </div>
                                </div>
                                <div class="col-md-6">
                                    <div class="row align-items-center">
                                        <label class="col-sm-4 col-form-label">Number of staff member participated(Provide list of staff members with  their EMPLOYEE ID & Certificates)<span class="ms-1" style="color: red;">*</span><span class="fa-solid fa-circle-info" data-bs-toggle="tooltip" data-bs-placement="top" title="${fieldInfo['Not Applicable']}"></span></label>
                                        <div class="col-sm-8">
                                            <input type="number" class="form-control" placeholder="Enter details" name = "nosmp" required>
                                        </div>
                                    </div>
                                </div>
                                <div class="col-md-4">
                                    <div class="row align-items-center">
                                        <label class="col-sm-4 col-form-label">Event report attached in proper format(YES/NO)<span class="ms-1" style="color: red;">*</span><span class="fa-solid fa-circle-info" data-bs-toggle="tooltip" data-bs-placement="top" title="${fieldInfo['Event report attached in proper format']}"></span></label>
                                        <div class="col-sm-8">
                                            <div class="d-flex column-gap-4">
                                                <div class="form-check">
                                                    <input type="radio" class="form-check-input" id="radio5" name="optradio4" value="y" required>
                                                    <label class="form-check-label" for="radio5">Yes</label>
                                                </div>
                                                <div class="form-check">
                                                    <input type="radio" class="form-check-input" id="radio6" name="optradio4" value="N">
                                                    <label class="form-check-label" for="radio6">No</label>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                                <div class="col-md-6">
                                    <div class="row align-items-center">
                                        <label class="col-sm-4 col-form-label">Upload Certificate/Proof(Only PDF)<span class="ms-1" style="color: red;">*</span><span class="fa-solid fa-circle-info" data-bs-toggle="tooltip" data-bs-placement="top" title="${fieldInfo['Upload Event Report']}"></span></label>
                                        <div class="col-sm-6">
                                            <input type="file" class="form-control" placeholder="Upload files" accept=".pdf" name="proof_file" required>
                                        </div>
                                    </div>
                                </div>
                                <div class="col-md-2 mt-5">
                                    <div class="row align-items-center">
                                        <div class="col-sm-8">
                                            <button type = "button" class="btn btn-primary"><i class="fa-solid fa-eye"></i>View</button>
                                        </div>
                                    </div>
                                </div>
                                <div class="col-md-6">
                                    <div class="row align-items-center">
                                        <label class="col-sm-4 col-form-label">Remarks(If any)</label>
                                        <div class="col-sm-8">
                                            <input type="text" class="form-control" placeholder="Enter Remarks" name = "remarks">
                                        </div>
                                    </div>
                                </div>
                                <div class = "col-md-12">
                                    <div class="row align-items-center justify-content-center">
                                        <button type = "submit" class="btn btn-primary rounded-pill" style = "width: 10%;">Submit</button>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <hr>
                    `;
                } else if(form_number == 4) {
                    subForm.innerHTML = `
                        <div class="sub-form-title" style = "font-size: 1.5rem; color: #667eea;"><b>${category} #${i}</b></div>
                        <input type = "hidden" name = "category" value = "${categoryValue[category]}">
                        <input type = "hidden" name = "csrfmiddlewaretoken" value = "${csrfToken}">
                        <div class="sub-form-fields">
                            <div class="row g-3">
                                <div class="col-md-4">
                                    <div class="row align-items-center">
                                        <label for="top" class="col-sm-4 col-form-label">Name of the Award/   Achievement<span class="ms-1" style="color: red;">*</span><span class="fa-solid fa-circle-info" data-bs-toggle="tooltip" data-bs-placement="top" title="${fieldInfo['Name of the Award/Achievement']}"></span></label>
                                        <div class = "col-md-8">
                                            <input type="text" class="form-control custom-back" id="top" placeholder="Enter name of award / achievement" name="noaa" required>
                                        </div>
                                    </div>
                                </div>
                                <div class="col-md-4">
                                    <div class="row align-items-center">
                                        <label class="col-sm-4 col-form-label">Position / Award For<span class="ms-1" style="color: red;">*</span><span class="fa-solid fa-circle-info" data-bs-toggle="tooltip" data-bs-placement="top" title="${fieldInfo['Position / Award For']}"></span></label>
                                        <div class="col-sm-8">
                                            <input type="text" class="form-control" placeholder="Enter award for" name = "paf" required>
                                        </div>
                                    </div>
                                </div>
                                <div class="col-md-4">
                                    <div class="row align-items-center">
                                        <label class="col-sm-4 col-form-label">Agency / Organization<span class="ms-1" style="color: red;">*</span><span class="fa-solid fa-circle-info" data-bs-toggle="tooltip" data-bs-placement="top" title="${fieldInfo['Agency / Organization']}"></span></label>
                                        <div class="col-sm-8">
                                            <input type="text" class="form-control" placeholder="Enter organizer" name = "ao" required>
                                        </div>
                                    </div>
                                </div>
                                <div class="col-md-4">
                                    <div class="row align-items-center">
                                        <label class="col-sm-4 col-form-label">Prize<span class="ms-1" style="color: red;">*</span><span class="fa-solid fa-circle-info" data-bs-toggle="tooltip" data-bs-placement="top" title="${fieldInfo['Prize']}"></span></label>
                                        <div class="col-sm-8">
                                            <input type="text" class="form-control" placeholder="Enter organizer" name = "prize" required>
                                        </div>
                                    </div>
                                </div>
                                <div class="col-md-4">
                                    <div class="row align-items-center">
                                        <label class="col-sm-4 col-form-label">Award Date<span class="ms-1" style="color: red;">*</span></label>
                                        <div class="col-sm-8">
                                            <input type="date" class="form-control" name = "award_date" required>
                                        </div>
                                    </div>
                                </div>
                                <div class="col-md-4">
                                    <div class="row align-items-center">
                                        <label class="col-sm-4 col-form-label">Remark<span class="ms-1" style="color: red;">*</span><span class="fa-solid fa-circle-info" data-bs-toggle="tooltip" data-bs-placement="top" title="${fieldInfo['Remark']}"></span></label>
                                        <div class="col-sm-8">
                                            <input type="text" class="form-control" placeholder="Enter organizer" name = "remark" required>
                                        </div>
                                    </div>
                                </div>
                                <div class="col-md-6">
                                    <div class="row align-items-center">
                                        <label class="col-sm-4 col-form-label">Upload Certificate/Proof(Only PDF)<span class="ms-1" style="color: red;">*</span><span class="fa-solid fa-circle-info" data-bs-toggle="tooltip" data-bs-placement="top" title="${fieldInfo['Upload Certificate/Proof']}"></span></label>
                                        <div class="col-sm-6">
                                            <input type="file" class="form-control" placeholder="Upload files" accept=".pdf" name="proof_file" required>
                                        </div>
                                    </div>
                                </div>
                                <div class="col-md-2" style = "margin-top: 2.5rem;">
                                    <div class="row align-items-center">
                                        <div class="col-sm-8">
                                            <button type = "button" class="btn btn-primary"><i class="fa-solid fa-eye"></i>View</button>
                                        </div>
                                    </div>
                                </div>

                                <div class="col-md-4" style = "margin-top: 2.5rem;">
                                    <div class="row align-items-center">
                                        <label class="col-sm-4 col-form-label">Session<span class="ms-1" style="color: red;">*</span><span class="fa-solid fa-circle-info" data-bs-toggle="tooltip" data-bs-placement="top" title="${fieldInfo['Session']}"></span></label>
                                        <div class="col-sm-8">
                                            <select class="form-control custom-back-select" name="sessionyear" id="sessionyear" required>
                                                <option value="" selected disabled>Select your Session</option>
                                                <option value="2025-26">2025-26</option>
                                                <option value="2026-27">2026-27</option>
                                                <option value="2027-28">2027-28</option>
                                                <option value="2028-29">2028-29</option>
                                                <option value="2029-30">2029-30</option>
                                            </select>
                                        </div>
                                    </div>
                                </div>
                                <div class="col-md-12">
                                    <div class="row align-items-center">
                                        <label class="col-sm-8 col-form-label">All information filled by me is correct and I will submit proof and other related document whenever is asked<span class="ms-1" style="color: red;">*</span></label>
                                        <div class="col-sm-4">
                                            <input type="checkbox" class="form-check-input" name = "num_of_days" required>
                                        </div>
                                    </div>
                                </div>
                                <div class = "col-md-12">
                                    <div class="row align-items-center justify-content-center">
                                        <button type = "submit" class="btn btn-primary rounded-pill" style = "width: 10%;">Submit</button>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <hr>
                    `;
                } else if (form_number == 5) {
                    subForm.innerHTML = `
                        <div class="sub-form-title" style = "font-size: 1.5rem; color: #667eea;"><b>${category} #${i}</b></div>
                        <input type = "hidden" name = "category" value = "${categoryValue[category]}">
                        <input type = "hidden" name = "csrfmiddlewaretoken" value = "${csrfToken}">
                        <div class="sub-form-fields">
                            <div class="row g-3">
                                <div class="col-md-4">
                                    <div class="row align-items-center">
                                        <label for="top" class="col-sm-4 col-form-label">Name of the Funding Agency</label>
                                        <div class = "col-md-8">
                                            <input type="text" class="form-control custom-back" id="nofa" placeholder="Enter title of the program" name="nofa" required>
                                        </div>
                                    </div>
                                </div>
                                <div class="col-md-4">
                                    <div class="row align-items-center">
                                        <label class="col-sm-4 col-form-label">Duration of Project (in Years)<span class="ms-1" style="color: red;">*</span></label>
                                        <div class="col-sm-8">
                                            <input type="number" class="form-control" placeholder="Enter organizer" name = "dop" required>
                                        </div>
                                    </div>
                                </div>
                                <div class="col-md-4">
                                    <div class="row align-items-center">
                                        <label class="col-sm-4 col-form-label">Amount in Rs.<span class="ms-1" style="color: red;">*</span></label>
                                        <div class="col-sm-8">
                                            <input type="number" class="form-control" placeholder="Enter organizer" name = "amount" required>
                                        </div>
                                    </div>
                                </div>
                                <div class="col-md-4">
                                    <div class="row align-items-center">
                                        <label class="col-sm-4 col-form-label">Session<span class="ms-1" style="color: red;">*</span><span class="fa-solid fa-circle-info" data-bs-toggle="tooltip" data-bs-placement="top" title="${fieldInfo['Session']}"></span></label>
                                        <div class="col-sm-8">
                                            <select class="form-control custom-back-select" name="sessionyear" id="sessionyear" required>
                                                <option value="" selected disabled>Select your Session</option>
                                                <option value="2025-26">2025-26</option>
                                                <option value="2026-27">2026-27</option>
                                                <option value="2027-28">2027-28</option>
                                                <option value="2028-29">2028-29</option>
                                                <option value="2029-30">2029-30</option>
                                            </select>
                                        </div>
                                    </div>
                                </div>
                                <div class="col-md-4">
                                    <div class="row align-items-center">
                                        <label class="col-sm-4 col-form-label">Status<span class="ms-1" style="color: red;">*</span></label>
                                        <div class="col-sm-8">
                                            <div class="d-flex column-gap-4">
                                                <div class="form-check">
                                                    <input type="radio" class="form-check-input" id="radio5" name="optradio2" value="ON" required>
                                                    <label class="form-check-label" for="radio5">Ongoing</label>
                                                </div>
                                                <div class="form-check">
                                                    <input type="radio" class="form-check-input" id="radio6" name="optradio2" value="CM">
                                                    <label class="form-check-label" for="radio6">Completed</label>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                                <div class="col-md-6">
                                    <div class="row align-items-center">
                                        <label class="col-sm-4 col-form-label">Upload Proof(Only PDF)<span class="ms-1" style="color: red;">*</span><span class="fa-solid fa-circle-info" data-bs-toggle="tooltip" data-bs-placement="top" title="${fieldInfo['Upload Proof']}"></span></label>
                                        <div class="col-sm-6">
                                            <input type="file" class="form-control" placeholder="Upload files" accept=".pdf" name="proof_file" required>
                                        </div>
                                    </div>
                                </div>
                                <div class="col-md-2 mt-5">
                                    <div class="row align-items-center">
                                        <div class="col-sm-8">
                                            <button type = "button" class="btn btn-primary"><i class="fa-solid fa-eye"></i>View</button>
                                        </div>
                                    </div>
                                </div>
                                <div class = "col-md-12">
                                    <div class="row align-items-center justify-content-center">
                                        <button type = "submit" class="btn btn-primary rounded-pill" style = "width: 10%;">Submit</button>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <hr>
                    `;
                } else if(form_number == 6) {
                    subForm.innerHTML = `
                        <div class="sub-form-title" style = "font-size: 1.5rem; color: #667eea;"><b>${category} #${i}</b></div>
                        <input type = "hidden" name = "csrfmiddlewaretoken" value = "${csrfToken}">
                        <div class="sub-form-fields">
                            <div class="row g-3">
                                <div class="col-md-4">
                                    <div class="row align-items-center">
                                        <label for="top" class="col-sm-4 col-form-label">Name of the author(s)<span class="ms-1" style="color: red;">*</span></label>
                                        <div class = "col-md-8">
                                            <input type="text" class="form-control" id="toc" placeholder="Enter name of author" name="noa" required>
                                        </div>
                                    </div>
                                </div>
                                <div class="col-md-4">
                                    <div class="row align-items-center">
                                        <label class="col-sm-4 col-form-label">Title of Paper<span class="ms-1" style="color: red;">*</span></label>
                                        <div class = "col-sm-8">
                                            <input type="text" class="form-control" placeholder="Enter title of Paper" name = "top" required>
                                        </div>
                                    </div>
                                </div>
                                <div class="col-md-4">
                                    <div class="row align-items-center">
                                        <label class="col-sm-4 col-form-label">Name of Journal<span class="ms-1" style="color: red;">*</span></label>
                                        <div class = "col-sm-8">
                                            <input type="text" class="form-control" placeholder="Enter name of journal" name = "noj" required>
                                        </div>
                                    </div>
                                </div>
                                <div class="col-md-4">
                                    <div class="row align-items-center">
                                        <label class="col-sm-4 col-form-label">Name of the Publisher<span class="ms-1" style="color: red;">*</span></label>
                                        <div class = "col-sm-8">
                                            <input type="text" class="form-control" placeholder="Enter name of publisher" name = "nop" required>
                                        </div>
                                    </div>
                                </div>
                                <div class="col-md-4">
                                    <div class="row align-items-center">
                                        <label class="col-sm-4 col-form-label">Volume, Issue<span class="ms-1" style="color: red;">*</span></label>
                                        <div class = "col-sm-8">
                                            <input type="text" class="form-control" placeholder="Enter volumn, issue" name = "vi" required>
                                        </div>
                                    </div>
                                </div>
                                <div class="col-md-4">
                                    <div class="row align-items-center">
                                        <label class="col-sm-4 col-form-label">Page No.<span class="ms-1" style="color: red;">*</span></label>
                                        <div class = "col-sm-8">
                                            <input type="number" class="form-control" placeholder="Enter page no." name = "pn" required>
                                        </div>
                                    </div>
                                </div>
                                <div class="col-md-4">
                                    <div class="row align-items-center">
                                        <label class="col-sm-4 col-form-label">Published Date<span class="ms-1" style="color: red;">*</span></label>
                                        <div class="col-sm-8">
                                            <input type="date" class="form-control" name = "begi_date" required>
                                        </div>
                                    </div>
                                </div>
                                <div class="col-md-4">
                                    <div class="row align-items-center">
                                        <label class="col-sm-4 col-form-label">Academic Session<span class="ms-1" style="color: red;">*</span><span class="fa-solid fa-circle-info" data-bs-toggle="tooltip" data-bs-placement="top" title="${fieldInfo['Session']}"></span></label>
                                        <div class="col-sm-8">
                                            <select class="form-control custom-back-select" name="sessionyear" id="sessionyear" required>
                                                <option value="" selected disabled>Select your Session</option>
                                                <option value="2025-26">2025-26</option>
                                                <option value="2026-27">2026-27</option>
                                                <option value="2027-28">2027-28</option>
                                                <option value="2028-29">2028-29</option>
                                                <option value="2029-30">2029-30</option>
                                            </select>
                                        </div>
                                    </div>
                                </div>
                                <div class="col-md-4">
                                    <div class="row align-items-center">
                                        <label class="col-sm-4 col-form-label">ISSN number : Print<span class="ms-1" style="color: red;">*</span><span class="fa-solid fa-circle-info" data-bs-toggle="tooltip" data-bs-placement="top" title="${fieldInfo['Not Applicable']}"></span></label>
                                        <div class = "col-sm-8">
                                            <input type="text" class="form-control" placeholder="Enter details" name = "isnp" required>
                                        </div>
                                    </div>
                                </div>
                                <div class="col-md-4">
                                    <div class="row align-items-center">
                                        <label class="col-sm-4 col-form-label">ISSN number : Online<span class="ms-1" style="color: red;">*</span><span class="fa-solid fa-circle-info" data-bs-toggle="tooltip" data-bs-placement="top" title="${fieldInfo['Not Applicable']}"></span></label>
                                        <div class = "col-sm-8">
                                            <input type="text" class="form-control" placeholder="Enter details" name = "isno" required>
                                        </div>
                                    </div>
                                </div>
                                <div class="col-md-4">
                                    <div class="row align-items-center">
                                        <label class="col-sm-4 col-form-label">Level (National/ International)<span class="ms-1" style="color: red;">*</span></label>
                                        <div class="col-sm-8">
                                            <div class="d-flex column-gap-4">
                                                <div class="form-check">
                                                    <input type="radio" class="form-check-input" id="radio1" name="optradio3" value="Na" required>
                                                    <label class="form-check-label" for="radio1">National</label>
                                                </div>
                                                <div class="form-check">
                                                    <input type="radio" class="form-check-input" id="radio2" name="optradio3" value="In">
                                                    <label class="form-check-label" for="radio2">International</label>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                                <div class="col-md-4">
                                    <div class="row align-items-center">
                                        <label class="col-sm-4 col-form-label">DOI(Digital Object Identifier)<span class="ms-1" style="color: red;">*</span><span class="fa-solid fa-circle-info" data-bs-toggle="tooltip" data-bs-placement="top" title="${fieldInfo['DOI']}"></span></label>
                                        <div class = "col-sm-8">
                                            <input type="text" class="form-control" placeholder="Enter DOI(Digital Object Identifier)" name = "doi" required>
                                        </div>
                                    </div>
                                </div>
                                <div class="col-md-4">
                                    <div class="row align-items-center">
                                        <label class="col-sm-4 col-form-label">Link to website of the Journal<span class="ms-1" style="color: red;">*</span><span class="fa-solid fa-circle-info" data-bs-toggle="tooltip" data-bs-placement="top" title="${fieldInfo['Link to website of the Journal']}"></span></label>
                                        <div class = "col-sm-8">
                                            <input type="text" class="form-control" placeholder="Enter DOI(Digital Object Identifier)" name = "lwj" required>
                                        </div>
                                    </div>
                                </div>
                                <div class="col-md-4">
                                    <div class="row align-items-center">
                                        <label class="col-sm-4 col-form-label">Link to article/paper/ abstract of the article<span class="ms-1" style="color: red;">*</span><span class="fa-solid fa-circle-info" data-bs-toggle="tooltip" data-bs-placement="top" title="${fieldInfo['Link to article/paper/abstract of the article']}"></span></label>
                                        <div class = "col-sm-8">
                                            <input type="text" class="form-control" placeholder="Enter Link to article/paper/abstract of the article " name = "lap" required>
                                        </div>
                                    </div>
                                </div>
                                <div class="col-md-4">
                                    <div class="row align-items-center">
                                        <label class="col-sm-4 col-form-label">Link to the recognition in SCOPUS enlistment of the Journal<span class="ms-1" style="color: red;">*</span></label>
                                        <div class = "col-sm-8">
                                            <input type="text" class="form-control" placeholder="Enter Link to the recognition in SCOPUS enlistment of the Journal" name = "lrsj" required>
                                        </div>
                                    </div>
                                </div>
                                <div class="col-md-4">
                                    <div class="row align-items-center">
                                        <label class="col-sm-4 col-form-label">Affiliating Institute at the time of publication<span class="ms-1" style="color: red;">*</span><span class="fa-solid fa-circle-info" data-bs-toggle="tooltip" data-bs-placement="top" title="${fieldInfo['Affiliating Institute at the time of publication']}"></span></label>
                                        <div class = "col-sm-8">
                                            <input type="text" class="form-control" placeholder="Enter Affiliating Institute at the time of publication" name = "aiop" required>
                                        </div>
                                    </div>
                                </div>
                                <div class="col-md-4">
                                    <div class="row align-items-center">
                                        <label class="col-sm-4 col-form-label">Is SKIT student associated?<span class="ms-1" style="color: red;">*</span><span class="fa-solid fa-circle-info" data-bs-toggle="tooltip" data-bs-placement="top" title="${fieldInfo['Is SKIT student associated?']}"></span></label>
                                        <div class="col-sm-8">
                                            <div class="d-flex column-gap-4">
                                                <div class="form-check">
                                                    <input type="radio" class="form-check-input" id="radio5" name="optradio2" value="y" required>
                                                    <label class="form-check-label" for="radio5">Yes</label>
                                                </div>
                                                <div class="form-check">
                                                    <input type="radio" class="form-check-input" id="radio6" name="optradio2" value="N">
                                                    <label class="form-check-label" for="radio6">No</label>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                                <div class="col-md-4">
                                    <div class="row align-items-center">
                                        <label class="col-sm-4 col-form-label">If Yes , Write student(s) details (Program, Branch, RollNo/EnrollNo, Name)<span class="ms-1" style="color: red;">*</span><span class="fa-solid fa-circle-info" data-bs-toggle="tooltip" data-bs-placement="top" title="${fieldInfo['If Yes , Write student(s) details (Program, Branch, RollNo/EnrollNo, Name)']}"></span></label>
                                        <div class = "col-sm-8">
                                            <input type="text" class="form-control" placeholder="Enter Student details" name = "details" required>
                                        </div>
                                    </div>
                                </div>
                                <div class="col-md-7">
                                    <div class="row align-items-center">
                                        <label class="col-sm-3 col-form-label">Indexed by<span class="ms-1" style="color: red;">*</span></label>
                                        <div class="col-sm-9">
                                            <div class="d-flex column-gap-4">
                                                <div class="form-check">
                                                    <input type="radio" class="form-check-input" id="radio3" name="optradio1" value="S" required>
                                                    <label class="form-check-label" for="radio3">SCI/SCIE/SSCI</label>
                                                </div>
                                                <div class="form-check">
                                                    <input type="radio" class="form-check-input" id="radio4" name="optradio1" value="NS">
                                                    <label class="form-check-label" for="radio4">Scopus</label>
                                                </div>
                                                <div class="form-check">
                                                    <input type="radio" class="form-check-input" id="radio4" name="optradio1" value="ES">
                                                    <label class="form-check-label" for="radio5">ESCI</label>
                                                </div>
                                                <div class="form-check">
                                                    <input type="radio" class="form-check-input" id="radio4" name="optradio1" value="UGC">
                                                    <label class="form-check-label" for="radio6">UGC</label>
                                                </div>
                                                <div class="form-check">
                                                    <input type="radio" class="form-check-input" id="radio4" name="optradio1" value="Other">
                                                    <label class="form-check-label" for="radio7">Other</label>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                                <div class="col-md-5">
                                    <div class="row align-items-center">
                                        <label class="col-sm-4 col-form-label">Quartile<span class="ms-1" style="color: red;">*</span></label>
                                        <div class="col-sm-8">
                                            <div class="d-flex column-gap-4">
                                                <div class="form-check">
                                                    <input type="radio" class="form-check-input" id="radio3" name="optradio" value="Q1" required>
                                                    <label class="form-check-label" for="radio3">Q1</label>
                                                </div>
                                                <div class="form-check">
                                                    <input type="radio" class="form-check-input" id="radio4" name="optradio" value="Q2">
                                                    <label class="form-check-label" for="radio4">Q2</label>
                                                </div>
                                                <div class="form-check">
                                                    <input type="radio" class="form-check-input" id="radio4" name="optradio" value="Q3">
                                                    <label class="form-check-label" for="radio5">Q3</label>
                                                </div>
                                                <div class="form-check">
                                                    <input type="radio" class="form-check-input" id="radio4" name="optradio" value="Q4">
                                                    <label class="form-check-label" for="radio6">Q4</label>
                                                </div>
                                                <div class="form-check">
                                                    <input type="radio" class="form-check-input" id="radio4" name="optradio" value="NA">
                                                    <label class="form-check-label" for="radio7">NA</label>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                                <div class="col-md-6">
                                    <div class="row align-items-center">
                                        <label class="col-sm-4 col-form-label">Upload Full Paper<span class="ms-1" style="color: red;">*</span><span class="fa-solid fa-circle-info" data-bs-toggle="tooltip" data-bs-placement="top" title="${fieldInfo['Upload Full Paper']}"></span></label>
                                        <div class="col-sm-6">
                                            <input type="file" class="form-control" accept=".pdf" name="proof_file" required>
                                        </div>
                                    </div>
                                </div>
                                <div class="col-md-2">
                                    <div class="row align-items-center">
                                        <div class="col-sm-8">
                                            <button type = "button" class="btn btn-primary"><i class="fa-solid fa-eye"></i>View</button>
                                        </div>
                                    </div>
                                </div>
                                <div class = "col-md-12">
                                    <div class="row align-items-center justify-content-center">
                                        <button type = "submit" class="btn btn-primary rounded-pill" style = "width: 10%;">Submit</button>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <hr>
                    `;
                } else if(form_number == 7) {
                    subForm.innerHTML = `
                        <div class="sub-form-title" style = "font-size: 1.5rem; color: #667eea;"><b>${category} #${i}</b></div>
                        <input type = "hidden" name = "csrfmiddlewaretoken" value = "${csrfToken}">
                        <div class="sub-form-fields">
                            <div class="row g-3">
                                <div class="col-md-4">
                                    <div class="row align-items-center">
                                        <label for="top" class="col-sm-4 col-form-label">Name of the author(s)<span class="ms-1" style="color: red;">*</span></label>
                                        <div class = "col-md-8">
                                            <input type="text" class="form-control" id="toc" placeholder="Enter name of author" name="noa" required>
                                        </div>
                                    </div>
                                </div>
                                <div class="col-md-4">
                                    <div class="row align-items-center">
                                        <label class="col-sm-4 col-form-label">Title of Conference<span class="ms-1" style="color: red;">*</span><span class="fa-solid fa-circle-info" data-bs-toggle="tooltip" data-bs-placement="top" title="${fieldInfo['Title of the Conference']}"></label>
                                        <div class = "col-sm-8">
                                            <input type="text" class="form-control" placeholder="Enter Title of the conference" name = "toc" required>
                                        </div>
                                    </div>
                                </div>
                                <div class="col-md-4">
                                    <div class="row align-items-center">
                                        <label class="col-sm-4 col-form-label">Title of Paper<span class="ms-1" style="color: red;">*</span></label>
                                        <div class = "col-sm-8">
                                            <input type="text" class="form-control" placeholder="Enter title of Paper" name = "top" required>
                                        </div>
                                    </div>
                                </div>
                                <div class="col-md-4">
                                    <div class="row align-items-center">
                                        <label class="col-sm-4 col-form-label">Title of the proceedings of the conference<span class="ms-1" style="color: red;">*</span><span class="fa-solid fa-circle-info" data-bs-toggle="tooltip" data-bs-placement="top" title="${fieldInfo['Title of the proceedings of the conference']}"></label>
                                        <div class = "col-sm-8">
                                            <input type="text" class="form-control" placeholder="Enter Title of the proceedings of the conference" name = "topc" required>
                                        </div>
                                    </div>
                                </div>
                                <div class="col-md-4">
                                    <div class="row align-items-center">
                                        <label class="col-sm-4 col-form-label">Level (National/ International)<span class="ms-1" style="color: red;">*</span></label>
                                        <div class="col-sm-8">
                                            <div class="d-flex column-gap-4">
                                                <div class="form-check">
                                                    <input type="radio" class="form-check-input" id="radio1" name="optradio3" value="Na" required>
                                                    <label class="form-check-label" for="radio1">National</label>
                                                </div>
                                                <div class="form-check">
                                                    <input type="radio" class="form-check-input" id="radio2" name="optradio3" value="In">
                                                    <label class="form-check-label" for="radio2">International</label>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                                <div class="col-md-4">
                                    <div class="row align-items-center">
                                        <label class="col-sm-4 col-form-label">ISBN/ISSN number of the proceeding<span class="ms-1" style="color: red;">*</span></label>
                                        <div class = "col-sm-8">
                                            <input type="text" class="form-control" placeholder="Enter ISBN/ISSN number of the proceeding" name = "isnp" required>
                                        </div>
                                    </div>
                                </div>
                                <div class="col-md-4">
                                    <div class="row align-items-center">
                                        <label class="col-sm-4 col-form-label">Name of the Publisher<span class="ms-1" style="color: red;">*</span></label>
                                        <div class = "col-sm-8">
                                            <input type="text" class="form-control" placeholder="Enter name of publisher" name = "nop" required>
                                        </div>
                                    </div>
                                </div>
                                <div class="col-md-4">
                                    <div class="row align-items-center">
                                        <label class="col-sm-4 col-form-label">Published Date<span class="ms-1" style="color: red;">*</span></label>
                                        <div class="col-sm-8">
                                            <input type="date" class="form-control" name = "begi_date" required>
                                        </div>
                                    </div>
                                </div>
                                <div class="col-md-4">
                                    <div class="row align-items-center">
                                        <label class="col-sm-4 col-form-label">Academic Session<span class="ms-1" style="color: red;">*</span><span class="fa-solid fa-circle-info" data-bs-toggle="tooltip" data-bs-placement="top" title="${fieldInfo['Session']}"></span></label>
                                        <div class="col-sm-8">
                                            <select class="form-control custom-back-select" name="sessionyear" id="sessionyear" required>
                                                <option value="" selected disabled>Select your Session</option>
                                                <option value="2025-26">2025-26</option>
                                                <option value="2026-27">2026-27</option>
                                                <option value="2027-28">2027-28</option>
                                                <option value="2028-29">2028-29</option>
                                                <option value="2029-30">2029-30</option>
                                            </select>
                                        </div>
                                    </div>
                                </div>
                                <div class="col-md-4">
                                    <div class="row align-items-center">
                                        <label class="col-sm-4 col-form-label">DOI(Digital Object Identifier)<span class="ms-1" style="color: red;">*</span><span class="fa-solid fa-circle-info" data-bs-toggle="tooltip" data-bs-placement="top" title="${fieldInfo['DOI']}"></span></label>
                                        <div class = "col-sm-8">
                                            <input type="text" class="form-control" placeholder="Enter DOI(Digital Object Identifier)" name = "doi" required>
                                        </div>
                                    </div>
                                </div>
                                <div class="col-md-4">
                                    <div class="row align-items-center">
                                        <label class="col-sm-4 col-form-label">Link to website of the Journal<span class="ms-1" style="color: red;">*</span><span class="fa-solid fa-circle-info" data-bs-toggle="tooltip" data-bs-placement="top" title="${fieldInfo['Link to website of the Journal']}"></span></label>
                                        <div class = "col-sm-8">
                                            <input type="text" class="form-control" placeholder="Enter Link to website of the Journal" name = "lwj" required>
                                        </div>
                                    </div>
                                </div>
                                <div class="col-md-4">
                                    <div class="row align-items-center">
                                        <label class="col-sm-4 col-form-label">Affiliating Institute at the time of publication<span class="ms-1" style="color: red;">*</span><span class="fa-solid fa-circle-info" data-bs-toggle="tooltip" data-bs-placement="top" title="${fieldInfo['Affiliating Institute at the time of publication']}"></span></label>
                                        <div class = "col-sm-8">
                                            <input type="text" class="form-control" placeholder="Enter Affiliating Institute at the time of publication" name = "aitp" required>
                                        </div>
                                    </div>
                                </div>
                                <div class="col-md-4">
                                    <div class="row align-items-center">
                                        <label class="col-sm-4 col-form-label">Is SKIT student associated?<span class="ms-1" style="color: red;">*</span><span class="fa-solid fa-circle-info" data-bs-toggle="tooltip" data-bs-placement="top" title="${fieldInfo['Is SKIT student associated?']}"></span></label>
                                        <div class="col-sm-8">
                                            <div class="d-flex column-gap-4">
                                                <div class="form-check">
                                                    <input type="radio" class="form-check-input" id="radio5" name="optradio2" value="y" required>
                                                    <label class="form-check-label" for="radio5">Yes</label>
                                                </div>
                                                <div class="form-check">
                                                    <input type="radio" class="form-check-input" id="radio6" name="optradio2" value="N">
                                                    <label class="form-check-label" for="radio6">No</label>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                                <div class="col-md-4">
                                    <div class="row align-items-center">
                                        <label class="col-sm-4 col-form-label">If Yes , Write student(s) details (Program, Branch, RollNo/EnrollNo, Name)<span class="ms-1" style="color: red;">*</span><span class="fa-solid fa-circle-info" data-bs-toggle="tooltip" data-bs-placement="top" title="${fieldInfo['If Yes , Write student(s) details (Program, Branch, RollNo/EnrollNo, Name)']}"></span></label>
                                        <div class = "col-sm-8">
                                            <input type="text" class="form-control" placeholder="Enter Student details" name = "details" required>
                                        </div>
                                    </div>
                                </div>
                                <div class="col-md-7">
                                    <div class="row align-items-center">
                                        <label class="col-sm-3 col-form-label">Indexed by<span class="ms-1" style="color: red;">*</span></label>
                                        <div class="col-sm-9">
                                            <div class="d-flex column-gap-4">
                                                <div class="form-check">
                                                    <input type="radio" class="form-check-input" id="radio3" name="optradio1" value="S" required>
                                                    <label class="form-check-label" for="radio3">SCI/SCIE/SSCI</label>
                                                </div>
                                                <div class="form-check">
                                                    <input type="radio" class="form-check-input" id="radio4" name="optradio1" value="NS">
                                                    <label class="form-check-label" for="radio4">Scopus</label>
                                                </div>
                                                <div class="form-check">
                                                    <input type="radio" class="form-check-input" id="radio4" name="optradio1" value="NS">
                                                    <label class="form-check-label" for="radio5">ESCI</label>
                                                </div>
                                                <div class="form-check">
                                                    <input type="radio" class="form-check-input" id="radio4" name="optradio1" value="NS">
                                                    <label class="form-check-label" for="radio6">UGC</label>
                                                </div>
                                                <div class="form-check">
                                                    <input type="radio" class="form-check-input" id="radio4" name="optradio1" value="NS">
                                                    <label class="form-check-label" for="radio7">Other</label>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                                <div class="col-md-6">
                                    <div class="row align-items-center">
                                        <label class="col-sm-4 col-form-label">Upload Full Paper<span class="ms-1" style="color: red;">*</span><span class="fa-solid fa-circle-info" data-bs-toggle="tooltip" data-bs-placement="top" title="${fieldInfo['Upload Full Paper']}"></span></label>
                                        <div class="col-sm-6">
                                            <input type="file" class="form-control" accept=".pdf" name="proof_file" required>
                                        </div>
                                    </div>
                                </div>
                                <div class="col-md-2">
                                    <div class="row align-items-center">
                                        <div class="col-sm-8">
                                            <button type = "button" class="btn btn-primary"><i class="fa-solid fa-eye"></i>View</button>
                                        </div>
                                    </div>
                                </div>
                                <div class = "col-md-12">
                                    <div class="row align-items-center justify-content-center">
                                        <button type = "submit" class="btn btn-primary rounded-pill" style = "width: 10%;">Submit</button>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <hr>
                    `;
                } else if(form_number == 8) {
                    subForm.innerHTML = `
                        <div class="sub-form-title" style = "font-size: 1.5rem; color: #667eea;"><b>${category} #${i}</b></div>
                        <input type = "hidden" name = "csrfmiddlewaretoken" value = "${csrfToken}">
                        <div class="sub-form-fields">
                            <div class="row g-3">
                                <div class="col-md-4">
                                    <div class="row align-items-center">
                                        <label for="top" class="col-sm-4 col-form-label">Name of the author(s)<span class="ms-1" style="color: red;">*</span></label>
                                        <div class = "col-md-8">
                                            <input type="text" class="form-control" id="toc" placeholder="Enter name of author" name="noa" required>
                                        </div>
                                    </div>
                                </div>
                                <div class="col-md-4">
                                    <div class="row align-items-center">
                                        <label class="col-sm-4 col-form-label">Title of the book<span class="ms-1" style="color: red;">*</span></label>
                                        <div class = "col-sm-8">
                                            <input type="text" class="form-control" placeholder="Enter Title of the conference" name = "tob" required>
                                        </div>
                                    </div>
                                </div>
                                <div class="col-md-4">
                                    <div class="row align-items-center">
                                        <label class="col-sm-4 col-form-label">Title of the chapter Published<span class="ms-1" style="color: red;">*</span><span class="fa-solid fa-circle-info" data-bs-toggle="tooltip" data-bs-placement="top" title="${fieldInfo['Not Applicable']}"></span></label>
                                        <div class = "col-sm-8">
                                            <input type="text" class="form-control" placeholder="Enter title of Paper" name = "top" required>
                                        </div>
                                    </div>
                                </div>
                                <div class="col-md-4">
                                    <div class="row align-items-center">
                                        <label class="col-sm-4 col-form-label">Level (National/ International)<span class="ms-1" style="color: red;">*</span></label>
                                        <div class="col-sm-8">
                                            <div class="d-flex column-gap-4">
                                                <div class="form-check">
                                                    <input type="radio" class="form-check-input" id="radio1" name="optradio3" value="Na" required>
                                                    <label class="form-check-label" for="radio1">National</label>
                                                </div>
                                                <div class="form-check">
                                                    <input type="radio" class="form-check-input" id="radio2" name="optradio3" value="In">
                                                    <label class="form-check-label" for="radio2">International</label>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                                <div class="col-md-4">
                                    <div class="row align-items-center">
                                        <label class="col-sm-4 col-form-label">ISBN<span class="ms-1" style="color: red;">*</span></label>
                                        <div class = "col-sm-8">
                                            <input type="text" class="form-control" placeholder="Enter ISBN" name = "isbn" required>
                                        </div>
                                    </div>
                                </div>
                                <div class="col-md-4">
                                    <div class="row align-items-center">
                                        <label class="col-sm-4 col-form-label">Name of the Publisher<span class="ms-1" style="color: red;">*</span></label>
                                        <div class = "col-sm-8">
                                            <input type="text" class="form-control" placeholder="Enter name of publisher" name = "nop" required>
                                        </div>
                                    </div>
                                </div>
                                <div class="col-md-4">
                                    <div class="row align-items-center">
                                        <label class="col-sm-4 col-form-label">Published Date<span class="ms-1" style="color: red;">*</span></label>
                                        <div class="col-sm-8">
                                            <input type="date" class="form-control" name = "begi_date" required>
                                        </div>
                                    </div>
                                </div>
                                <div class="col-md-4">
                                    <div class="row align-items-center">
                                        <label class="col-sm-4 col-form-label">Academic Session<span class="ms-1" style="color: red;">*</span><span class="fa-solid fa-circle-info" data-bs-toggle="tooltip" data-bs-placement="top" title="${fieldInfo['Session']}"></span></label>
                                        <div class="col-sm-8">
                                            <select class="form-control custom-back-select" name="sessionyear" id="sessionyear" required>
                                                <option value="" selected disabled>Select your Session</option>
                                                <option value="2025-26">2025-26</option>
                                                <option value="2026-27">2026-27</option>
                                                <option value="2027-28">2027-28</option>
                                                <option value="2028-29">2028-29</option>
                                                <option value="2029-30">2029-30</option>
                                            </select>
                                        </div>
                                    </div>
                                </div>
                                <div class="col-md-4">
                                    <div class="row align-items-center">
                                        <label class="col-sm-4 col-form-label">DOI(Digital Object Identifier)<span class="ms-1" style="color: red;">*</span><span class="fa-solid fa-circle-info" data-bs-toggle="tooltip" data-bs-placement="top" title="${fieldInfo['DOI']}"></span></label>
                                        <div class = "col-sm-8">
                                            <input type="text" class="form-control" placeholder="Enter DOI(Digital Object Identifier)" name = "doi" required>
                                        </div>
                                    </div>
                                </div>
                                <div class="col-md-4">
                                    <div class="row align-items-center">
                                        <label class="col-sm-4 col-form-label">Link to website of the Journal<span class="ms-1" style="color: red;">*</span><span class="fa-solid fa-circle-info" data-bs-toggle="tooltip" data-bs-placement="top" title="${fieldInfo['Link to website of the Journal']}"></span></label>
                                        <div class = "col-sm-8">
                                            <input type="text" class="form-control" placeholder="Enter Link to website of the Journal" name = "lwj" required>
                                        </div>
                                    </div>
                                </div>
                                <div class="col-md-8">
                                    <div class="row align-items-center">
                                        <label class="col-sm-4 col-form-label">Affiliating Institute at the time of publication<span class="ms-1" style="color: red;">*</span><span class="fa-solid fa-circle-info" data-bs-toggle="tooltip" data-bs-placement="top" title="${fieldInfo['Affiliating Institute at the time of publication']}"></span></label>
                                        <div class = "col-sm-8">
                                            <input type="text" class="form-control" placeholder="Enter Affiliating Institute at the time of publication" name = "aitp" required>
                                        </div>
                                    </div>
                                </div>
                                <div class="col-md-4">
                                    <div class="row align-items-center">
                                        <label class="col-sm-4 col-form-label">Is SKIT student associated?<span class="ms-1" style="color: red;">*</span><span class="fa-solid fa-circle-info" data-bs-toggle="tooltip" data-bs-placement="top" title="${fieldInfo['Is SKIT student associated?']}"></span></label>
                                        <div class="col-sm-8">
                                            <div class="d-flex column-gap-4">
                                                <div class="form-check">
                                                    <input type="radio" class="form-check-input" id="radio5" name="optradio2" value="y" required>
                                                    <label class="form-check-label" for="radio5">Yes</label>
                                                </div>
                                                <div class="form-check">
                                                    <input type="radio" class="form-check-input" id="radio6" name="optradio2" value="N">
                                                    <label class="form-check-label" for="radio6">No</label>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                                <div class="col-md-8">
                                    <div class="row align-items-center">
                                        <label class="col-sm-4 col-form-label">If Yes , Write student(s) details (Program, Branch, RollNo/EnrollNo, Name)<span class="ms-1" style="color: red;">*</span><span class="fa-solid fa-circle-info" data-bs-toggle="tooltip" data-bs-placement="top" title="${fieldInfo['If Yes , Write student(s) details (Program, Branch, RollNo/EnrollNo, Name)']}"></span></label>
                                        <div class = "col-sm-8">
                                            <input type="text" class="form-control" placeholder="Enter Student details" name = "details" required>
                                        </div>
                                    </div>
                                </div>
                                <div class="col-md-7">
                                    <div class="row align-items-center">
                                        <label class="col-sm-3 col-form-label">Indexed by<span class="ms-1" style="color: red;">*</span></label>
                                        <div class="col-sm-9">
                                            <div class="d-flex column-gap-4">
                                                <div class="form-check">
                                                    <input type="radio" class="form-check-input" id="radio3" name="optradio1" value="S" required>
                                                    <label class="form-check-label" for="radio3">SCI/SCIE/SSCI</label>
                                                </div>
                                                <div class="form-check">
                                                    <input type="radio" class="form-check-input" id="radio4" name="optradio1" value="NS">
                                                    <label class="form-check-label" for="radio4">Scopus</label>
                                                </div>
                                                <div class="form-check">
                                                    <input type="radio" class="form-check-input" id="radio5" name="optradio1" value="ES">
                                                    <label class="form-check-label" for="radio5">ESCI</label>
                                                </div>
                                                <div class="form-check">
                                                    <input type="radio" class="form-check-input" id="radio6" name="optradio1" value="UGC">
                                                    <label class="form-check-label" for="radio6">UGC</label>
                                                </div>
                                                <div class="form-check">
                                                    <input type="radio" class="form-check-input" id="radio7" name="optradio1" value="O">
                                                    <label class="form-check-label" for="radio7">Other</label>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                                <div class="col-md-6">
                                    <div class="row align-items-center">
                                        <label class="col-sm-4 col-form-label">Upload Full Paper<span class="ms-1" style="color: red;">*</span><span class="fa-solid fa-circle-info" data-bs-toggle="tooltip" data-bs-placement="top" title="${fieldInfo['Upload Full Paper']}"></span></label>
                                        <div class="col-sm-6">
                                            <input type="file" class="form-control" accept=".pdf" name="proof_file" required>
                                        </div>
                                    </div>
                                </div>
                                <div class="col-md-2">
                                    <div class="row align-items-center">
                                        <div class="col-sm-8">
                                            <button type = "button" class="btn btn-primary"><i class="fa-solid fa-eye"></i>View</button>
                                        </div>
                                    </div>
                                </div>
                                <div class = "col-md-12">
                                    <div class="row align-items-center justify-content-center">
                                        <button type = "submit" class="btn btn-primary rounded-pill" style = "width: 10%;">Submit</button>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <hr>
                    `;
                } else if (form_number == 9) {
                    subForm.innerHTML = `
                        <div class="sub-form-title" style = "font-size: 1.5rem; color: #667eea;"><b>${category} #${i}</b></div>
                        <input type = "hidden" name = "csrfmiddlewaretoken" value = "${csrfToken}">
                        <div class="sub-form-fields">
                            <div class="row g-3">
                                <div class="col-md-4">
                                    <div class="row align-items-center">
                                        <label class="col-sm-4 col-form-label">Status of Patent<span class="ms-1" style="color: red;">*</span><span class="fa-solid fa-circle-info" data-bs-toggle="tooltip" data-bs-placement="top" title="${fieldInfo['Is the Patent granted ?']}"></span></label>
                                        <div class="col-sm-8">
                                            <div class="d-flex column-gap-4">
                                                <div class="form-check">
                                                    <input type="radio" class="form-check-input" id="radio5" name="optradio1" value="P" required>
                                                    <label class="form-check-label" for="radio5">Published</label>
                                                </div>
                                                <div class="form-check">
                                                    <input type="radio" class="form-check-input" id="radio6" name="optradio1" value="G">
                                                    <label class="form-check-label" for="radio6">Granted</label>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                                <div class="col-md-4">
                                    <div class="row align-items-center">
                                        <label for="top" class="col-sm-4 col-form-label">Granted ID<span class="ms-1" style="color: red;">*</span></label>
                                        <div class = "col-md-8">
                                            <input type="text" class="form-control" id="toc" placeholder="Enter " name="nof" required>
                                        </div>
                                    </div>
                                </div>
                                <div class="col-md-4">
                                    <div class="row align-items-center">
                                        <label class="col-sm-4 col-form-label">Application ID<span class="ms-1" style="color: red;">*</span></label>
                                        <div class = "col-sm-8">
                                            <input type="text" class="form-control" placeholder="Enter ID" name = "ag" required>
                                        </div>
                                    </div>
                                </div>
                                <div class="col-md-4">
                                    <div class="row align-items-center">
                                        <label class="col-sm-4 col-form-label">Type of Patent<span class="ms-1" style="color: red;">*</span><span class="fa-solid fa-circle-info" data-bs-toggle="tooltip" data-bs-placement="top" title="${fieldInfo['Is the Patent granted ?']}"></span></label>
                                        <div class="col-sm-8">
                                            <div class="d-flex column-gap-4">
                                                <div class="form-check">
                                                    <input type="radio" class="form-check-input" id="radio5" name="optradio2" value="I" required>
                                                    <label class="form-check-label" for="radio5">Innovation</label>
                                                </div>
                                                <div class="form-check">
                                                    <input type="radio" class="form-check-input" id="radio6" name="optradio2" value="D">
                                                    <label class="form-check-label" for="radio6">Design</label>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                                <div class="col-md-4">
                                    <div class="row align-items-center">
                                        <label class="col-sm-4 col-form-label">Title of Patent<span class="ms-1" style="color: red;">*</span></label>
                                        <div class = "col-sm-8">
                                            <input type="text" class="form-control" placeholder="Enter title of Patent" name = "top" required>
                                        </div>
                                    </div>
                                </div>
                                <div class="col-md-4">
                                    <div class="row align-items-center">
                                        <label class="col-sm-4 col-form-label">Granted Country<span class="ms-1" style="color: red;">*</span></label>
                                        <div class = "col-sm-8">
                                            <input type="text" class="form-control" placeholder="Enter detail" name = "gc" required>
                                        </div>
                                    </div>
                                </div>
                                <div class="col-md-4">
                                    <div class="row align-items-center">
                                        <label class="col-sm-4 col-form-label">Patent Filed Date<span class="ms-1" style="color: red;">*</span></label>
                                        <div class="col-sm-8">
                                            <input type="date" class="form-control" name = "filed_date" required>
                                        </div>
                                    </div>
                                </div>
                                <div class="col-md-4">
                                    <div class="row align-items-center">
                                        <label class="col-sm-4 col-form-label">Publication Date<span class="ms-1" style="color: red;">*</span></label>
                                        <div class="col-sm-8">
                                            <input type="date" class="form-control" name = "begi_date" required>
                                        </div>
                                    </div>
                                </div>
                                <div class="col-md-4">
                                    <div class="row align-items-center">
                                        <label class="col-sm-4 col-form-label">Academic Session<span class="ms-1" style="color: red;">*</span><span class="fa-solid fa-circle-info" data-bs-toggle="tooltip" data-bs-placement="top" title="${fieldInfo['Session']}"></span></label>
                                        <div class="col-sm-8">
                                            <select class="form-control custom-back-select" name="sessionyear" id="sessionyear" required>
                                                <option value="" selected disabled>Select your Session</option>
                                                <option value="2025-26">2025-26</option>
                                                <option value="2026-27">2026-27</option>
                                                <option value="2027-28">2027-28</option>
                                                <option value="2028-29">2028-29</option>
                                                <option value="2029-30">2029-30</option>
                                            </select>
                                        </div>
                                    </div>
                                </div>

                                <div class="col-md-4">
                                    <div class="row align-items-center">
                                        <label class="col-sm-4 col-form-label">Is SKIT student associated?<span class="ms-1" style="color: red;">*</span><span class="fa-solid fa-circle-info" data-bs-toggle="tooltip" data-bs-placement="top" title="${fieldInfo['Is SKIT student associated?(Patent)']}"></span></label>
                                        <div class="col-sm-8">
                                            <div class="d-flex column-gap-4">
                                                <div class="form-check">
                                                    <input type="radio" class="form-check-input" id="radio5" name="optradio" value="y" required>
                                                    <label class="form-check-label" for="radio5">Yes</label>
                                                </div>
                                                <div class="form-check">
                                                    <input type="radio" class="form-check-input" id="radio6" name="optradio" value="N">
                                                    <label class="form-check-label" for="radio6">No</label>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                                <div class="col-md-4">
                                    <div class="row align-items-center">
                                        <label class="col-sm-4 col-form-label">If Yes , Write student(s) details (Program, Branch, RollNo/EnrollNo, Name)<span class="ms-1" style="color: red;">*</span><span class="fa-solid fa-circle-info" data-bs-toggle="tooltip" data-bs-placement="top" title="${fieldInfo['If Yes , Write student(s) details (Program, Branch, RollNo/EnrollNo, Name)']}"></span></label>
                                        <div class = "col-sm-8">
                                            <input type="text" class="form-control" placeholder="Enter Student details" name = "details" required>
                                        </div>
                                    </div>
                                </div>
                                <div class="col-md-4">
                                    <div class="row align-items-center">
                                        <label class="col-sm-4 col-form-label">Link<span class="ms-1" style="color: red;">*</span><span class="fa-solid fa-circle-info" data-bs-toggle="tooltip" data-bs-placement="top" title="${fieldInfo['Link to website of the Journal']}"></span></label>
                                        <div class = "col-sm-8">
                                            <input type="text" class="form-control" placeholder="Enter Link to website of the Journal" name = "link" required>
                                        </div>
                                    </div>
                                </div>
                                <div class="col-md-6">
                                    <div class="row align-items-center">
                                        <label class="col-sm-4 col-form-label">Upload Full Paper<span class="ms-1" style="color: red;">*</span><span class="fa-solid fa-circle-info" data-bs-toggle="tooltip" data-bs-placement="top" title="${fieldInfo['Upload Full Paper']}"></span></label>
                                        <div class="col-sm-6">
                                            <input type="file" class="form-control" accept=".pdf" name="proof_file" required>
                                        </div>
                                    </div>
                                </div>
                                <div class="col-md-2">
                                    <div class="row align-items-center">
                                        <div class="col-sm-8">
                                            <button type = "button" class="btn btn-primary"><i class="fa-solid fa-eye"></i>View</button>
                                        </div>
                                    </div>
                                </div>
                                <div class = "col-md-12">
                                    <div class="row align-items-center justify-content-center">
                                        <button type = "submit" class="btn btn-primary rounded-pill" style = "width: 10%;">Submit</button>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <hr>
                    `;
                } else if (form_number == 10) {
                    subForm.innerHTML = `
                        <div class="sub-form-title" style = "font-size: 1.5rem; color: #667eea;"><b>${category} #${i}</b></div>
                        <input type = "hidden" name = "category" value = "${categoryValue[category]}">
                        <input type = "hidden" name = "csrfmiddlewaretoken" value = "${csrfToken}">
                        <div class="sub-form-fields">
                            <div class="row g-3">
                                <div class="col-md-4">
                                    <div class="row align-items-center">
                                        <label for="top" class="col-sm-4 col-form-label">Name of the student Guided<span class="ms-1" style="color: red;">*</span></label>
                                        <div class = "col-md-8">
                                            <input type="text" class="form-control custom-back" id="top" placeholder="Enter Name of the student Guided" name="nos" required>
                                        </div>
                                    </div>
                                </div>
                                <div class="col-md-4">
                                    <div class="row align-items-center">
                                        <label class="col-sm-4 col-form-label">Enrollment Number of Student<span class="ms-1" style="color: red;">*</span></label>
                                        <div class="col-sm-8">
                                            <input type="text" class="form-control" placeholder="Enter Enrollment Number of Student" name = "ens" required>
                                        </div>
                                    </div>
                                </div>
                                <div class="col-md-4">
                                    <div class="row align-items-center">
                                        <label class="col-sm-4 col-form-label">University Roll Number of Student<span class="ms-1" style="color: red;">*</span></label>
                                        <div class="col-sm-8">
                                            <input type="text" class="form-control" placeholder="Enter organizer" name = "urns" required>
                                        </div>
                                    </div>
                                </div>
                                <div class="col-md-4">
                                    <div class="row align-items-center">
                                        <label class="col-sm-4 col-form-label">Enrollment Year of Student<span class="ms-1" style="color: red;">*</span></label>
                                        <div class="col-sm-8">
                                            <select class="form-control custom-back-select" name="enrollmentyear" id="enrollmentyear" required>
                                                <option value="" selected disabled>Select enrollment year</option>
                                                <option value="2023">2023</option>
                                                <option value="2024">2024</option>
                                                <option value="2025">2025</option>
                                            </select>
                                        </div>
                                    </div>
                                </div>
                                <div class="col-md-4">
                                    <div class="row align-items-center">
                                        <label class="col-sm-4 col-form-label">Title of the Dissertation<span class="ms-1" style="color: red;">*</span></label>
                                        <div class="col-sm-8">
                                            <input type="text" class="form-control" placeholder="Enter organizer" name = "tod" required>
                                        </div>
                                    </div>
                                </div>
                                <div class="col-md-4">
                                    <div class="row align-items-center">
                                        <label class="col-sm-4 col-form-label">Supervisor / Co-supervisor<span class="ms-1" style="color: red;">*</span></label>
                                        <div class="col-sm-8">
                                            <div class="d-flex column-gap-4">
                                                <div class="form-check">
                                                    <input type="radio" class="form-check-input" id="radio5" name="optradio2" value="S" required>
                                                    <label class="form-check-label" for="radio5">Supervisor</label>
                                                </div>
                                                <div class="form-check">
                                                    <input type="radio" class="form-check-input" id="radio6" name="optradio2" value="CS">
                                                    <label class="form-check-label" for="radio6">Co-supervisor</label>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                                <div class="col-md-4">
                                    <div class="row align-items-center">
                                        <label class="col-sm-4 col-form-label">Date of Viva-Voce<span class="ms-1" style="color: red;">*</span></label>
                                        <div class="col-sm-8">
                                            <input type="date" class="form-control" name = "dov" required>
                                        </div>
                                    </div>
                                </div>
                                 <div class="col-md-4">
                                    <div class="row align-items-center">
                                        <label class="col-sm-4 col-form-label">Name of external examiner<span class="ms-1" style="color: red;">*</span></label>
                                        <div class="col-sm-8">
                                            <input type="text" class="form-control" placeholder="Enter Name of external examiner" name = "noe" required>
                                        </div>
                                    </div>
                                </div>
                                <div class="col-md-4">
                                    <div class="row align-items-center">
                                        <label class="col-sm-4 col-form-label">Session<span class="ms-1" style="color: red;">*</span><span class="fa-solid fa-circle-info" data-bs-toggle="tooltip" data-bs-placement="top" title="${fieldInfo['Session']}"></span></label>
                                        <div class="col-sm-8">
                                            <select class="form-control custom-back-select" name="sessionyear" id="sessionyear" required>
                                                <option value="" selected disabled>Select your Session</option>
                                                <option value="2025-26">2025-26</option>
                                                <option value="2026-27">2026-27</option>
                                                <option value="2027-28">2027-28</option>
                                                <option value="2028-29">2028-29</option>
                                                <option value="2029-30">2029-30</option>
                                            </select>
                                        </div>
                                    </div>
                                </div>
                                <div class = "col-md-12">
                                    <div class="row align-items-center justify-content-center">
                                        <button type = "submit" class="btn btn-primary rounded-pill" style = "width: 10%;">Submit</button>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <hr>
                    `;
                } else if (form_number == 11) {
                    subForm.innerHTML = `
                        <div class="sub-form-title" style = "font-size: 1.5rem; color: #667eea;"><b>${category} #${i}</b></div>
                        <input type = "hidden" name = "category" value = "${categoryValue[category]}">
                        <input type = "hidden" name = "csrfmiddlewaretoken" value = "${csrfToken}">
                        <div class="sub-form-fields">
                            <div class="row g-3">
                                <div class="col-md-6">
                                    <div class="row align-items-center">
                                        <label for="top" class="col-sm-4 col-form-label">Title of Event/ Exam Name<span class="ms-1" style="color: red;">*</span><span class="fa-solid fa-circle-info" data-bs-toggle="tooltip" data-bs-placement="top" title="${fieldInfo['Title of Event/ Exam Name']}"></span></label>
                                        <div class = "col-md-8">
                                            <input type="text" class="form-control custom-back" id="top" placeholder="Enter Name of the student Guided" name="toe" required>
                                        </div>
                                    </div>
                                </div>
                                <div class="col-md-6">
                                    <div class="row align-items-center">
                                        <label class="col-sm-4 col-form-label">Subject Area/Subject Name/Lab Name/Session Name<span class="ms-1" style="color: red;">*</span><span class="fa-solid fa-circle-info" data-bs-toggle="tooltip" data-bs-placement="top" title="${fieldInfo['Subject Area/Subject Name/Lab Name/Session Name']}"></span></label>
                                        <div class="col-sm-8">
                                            <input type="text" class="form-control" placeholder="Enter Enrollment Number of Student" name = "sa" required>
                                        </div>
                                    </div>
                                </div>
                                <div class="col-md-6">
                                    <div class="row align-items-center">
                                        <label class="col-sm-4 col-form-label">Duration of event (in days)<span class="ms-1" style="color: red;">*</span></label>
                                        <div class="col-sm-8">
                                            <input type="number" class="form-control" placeholder="Enter no. of days" name = "doe" required>
                                        </div>
                                    </div>
                                </div>
                                <div class="col-md-12">
                                    <div class="row align-items-center">
                                        <label class="col-sm-2 col-form-label">Resource Person Type<span class="ms-1" style="color: red;">*</span></label>
                                        <div class="col-sm-10">
                                            <div class="d-flex column-gap-4">
                                                <div class="form-check">
                                                    <input type="radio" class="form-check-input" id="radio5" name="optradio2" value="EE(UG)" required>
                                                    <label class="form-check-label" for="radio5">External Examination (UG)</label>
                                                </div>
                                                <div class="form-check">
                                                    <input type="radio" class="form-check-input" id="radio6" name="optradio2" value="EE(PG)">
                                                    <label class="form-check-label" for="radio6">External Examination (PG)</label>
                                                </div>
                                                <div class="form-check">
                                                    <input type="radio" class="form-check-input" id="radio7" name="optradio2" value="EBM">
                                                    <label class="form-check-label" for="radio7">Editorial Board Member</label>
                                                </div>
                                                <div class="form-check">
                                                    <input type="radio" class="form-check-input" id="radio8" name="optradio2" value="JM">
                                                    <label class="form-check-label" for="radio8">Jury Member</label>
                                                </div>
                                                <div class="form-check">
                                                    <input type="radio" class="form-check-input" id="radio9" name="optradio2" value="R">
                                                    <label class="form-check-label" for="radio9">Reviewer</label>
                                                </div>
                                                <div class="form-check">
                                                    <input type="radio" class="form-check-input" id="radio10" name="optradio2" value="SC">
                                                    <label class="form-check-label" for="radio10">Session Chair</label>
                                                </div>
                                                <div class="form-check">
                                                    <input type="radio" class="form-check-input" id="radio11" name="optradio2" value="E">
                                                    <label class="form-check-label" for="radio11">Expert</label>
                                                </div>
                                                <div class="form-check">
                                                    <input type="radio" class="form-check-input" id="radio12" name="optradio2" value="S">
                                                    <label class="form-check-label" for="radio12">Speaker</label>
                                                </div>
                                                <div class="form-check">
                                                    <input type="radio" class="form-check-input" id="radio13" name="optradio2" value="KNS">
                                                    <label class="form-check-label" for="radio13">Key Note Speaker</label>
                                                </div>
                                            </div>
                                            <div class="d-flex column-gap-4 mt-3">
                                                <div class="form-check">
                                                    <input type="radio" class="form-check-input" id="radio6" name="optradio2" value="T">
                                                    <label class="form-check-label" for="radio6">Trainer</label>
                                                </div>
                                                <div class="form-check">
                                                    <input type="radio" class="form-check-input" id="radio6" name="optradio2" value="TCM">
                                                    <label class="form-check-label" for="radio6">Technical Committee Member</label>
                                                </div>
                                                <div class="form-check">
                                                    <input type="radio" class="form-check-input" id="radio6" name="optradio2" value="DET">
                                                    <label class="form-check-label" for="radio6">Delivered Expert Lecture/Talk</label>
                                                </div>
                                                <div class="form-check">
                                                    <input type="radio" class="form-check-input" id="radio6" name="optradio2" value="DIT">
                                                    <label class="form-check-label" for="radio6">Delivered Invited Talk</label>
                                                </div>
                                                <div class="form-check">
                                                    <input type="radio" class="form-check-input" id="radio6" name="optradio2" value="BM">
                                                    <label class="form-check-label" for="radio6">BOS Member</label>
                                                </div>
                                                <div class="form-check">
                                                    <input type="radio" class="form-check-input" id="radio6" name="optradio2" value="DM">
                                                    <label class="form-check-label" for="radio6">DRC Member</label>
                                                </div>
                                                <div class="form-check">
                                                    <input type="radio" class="form-check-input" id="radio6" name="optradio2" value="O">
                                                    <label class="form-check-label" for="radio6">Other</label>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                                <div class="col-md-4 mt-4">
                                    <div class="row align-items-center">
                                        <label class="col-sm-4 col-form-label">From Date<span class="ms-1" style="color: red;">*</span></label>
                                        <div class="col-sm-8">
                                            <input type="date" class="form-control" name = "begi_date" required>
                                        </div>
                                    </div>
                                </div>
                                <div class="col-md-4 mt-4">
                                    <div class="row align-items-center">
                                        <label class="col-sm-4 col-form-label">To Date<span class="ms-1" style="color: red;">*</span></label>
                                        <div class="col-sm-8">
                                            <input type="date" class="form-control" name = "end_date" required>
                                        </div>
                                    </div>
                                </div>
                                <div class="col-md-4 mt-4">
                                    <div class="row align-items-center">
                                        <label class="col-sm-4 col-form-label">Session<span class="ms-1" style="color: red;">*</span><span class="fa-solid fa-circle-info" data-bs-toggle="tooltip" data-bs-placement="top" title="${fieldInfo['Session']}"></span></label>
                                        <div class="col-sm-8">
                                            <select class="form-control custom-back-select" name="sessionyear" id="sessionyear" required>
                                                <option value="" selected disabled>Select your Session</option>
                                                <option value="2025-26">2025-26</option>
                                                <option value="2026-27">2026-27</option>
                                                <option value="2027-28">2027-28</option>
                                                <option value="2028-29">2028-29</option>
                                                <option value="2029-30">2029-30</option>
                                            </select>
                                        </div>
                                    </div>
                                </div>
                                <div class="col-md-4 mt-4">
                                    <div class="row align-items-center">
                                        <label class="col-sm-4 col-form-label">Venue<span class="ms-1" style="color: red;">*</span></label>
                                        <div class="col-sm-8">
                                            <input type="text" class="form-control" placeholder="Enter venue of event" name = "venue" required>
                                        </div>
                                    </div>
                                </div>
                                <div class="col-md-6 mt-4">
                                    <div class="row align-items-center">
                                        <label class="col-sm-5 col-form-label">Proof(Certificate/Mail)<span class="ms-1" style="color: red;">*</span><span class="fa-solid fa-circle-info" data-bs-toggle="tooltip" data-bs-placement="top" title="${fieldInfo['Proof (Certificate/Mail)']}"></span></label>
                                        <div class="col-sm-7">
                                            <input type="file" class="form-control" accept=".pdf" name="proof_file" required>
                                        </div>
                                    </div>
                                </div>
                                <div class="col-md-2 mt-4">
                                    <div class="row align-items-center">
                                        <div class="col-sm-8">
                                            <button type = "button" class="btn btn-primary"><i class="fa-solid fa-eye"></i>View</button>
                                        </div>
                                    </div>
                                </div>
                                <div class = "col-md-12 mt-4">
                                    <div class="row align-items-center justify-content-center">
                                        <button type = "submit" class="btn btn-primary rounded-pill" style = "width: 10%;">Submit</button>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <hr>
                    `;
                }
                subFormsContainer.appendChild(subForm);

                const tooltips = subForm.querySelectorAll('[data-bs-toggle="tooltip"]');
                tooltips.forEach(tooltip => {
                    new bootstrap.Tooltip(tooltip);
                });
            }
        }
    });

    if (!hasQuantity) {
        subFormsContainer.innerHTML = '<div class="empty-state">Enter quantities above to generate sub-forms</div>';
    }

    subformCount.textContent = `${totalForms} form${totalForms !== 1 ? 's' : ''}`;
}