const checkboxGroup = document.getElementById('checkboxGroup');
const inputFields = document.getElementById('inputFields');
const subFormsContainer = document.getElementById('subFormsContainer');
const inputCount = document.getElementById('inputCount');
const subformCount = document.getElementById('subformCount');
const emptyStateText = document.querySelector('.empty-state');
const regenerateBtn = document.getElementById('regenerateBtn');
const backToTopBtn = document.getElementById('backToTopBtn');

const quantities = {};
let formCounter = 0;
let currentCategory = "";
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
    'Upload Proof (Patent)': 'Rename file as session_name_patent for e.g : 2024-25_NikhilGupta_patent',
    'Title of Event/ Exam Name': 'for e.g. : University Practical Exam B.Tech CSE V Sem  2023-24, International Conference on AI Systems and Sustainable Technologies 2025, Name of the Journal if editorial board member etc.',
    'Subject Area/Subject Name/Lab Name/Session Name': 'for e.g: Object Oriented Programming Lab, Name of session',
    'Proof (Certificate/Mail)': 'Any proof in (certificate/mail screenshot/document/etc) which validates you as a resource person',
    'Actual Expenditure': 'Only write amount (will be considered in Rs. only)',
    'Mapped SDGs': 'Event Organized is mapped with which SDGs (Sustainable Development Goals) out of 17 SDGs given below? Select 1 or more options',
    'Title of the chapter Published': 'Write NA if not applicable i.e  If you are author/editor of complete book write NA.'
};

const categoryValue = {
    'FDP': 'FDP',
    'Workshop': 'WKP',
    'Conference': 'CON',
    'STTP': 'STTP',
    'Seminar': 'SEM',
    'Webinar': 'WEB',
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
    'MOOC': 'MOOC',
    'Induction Program': 'IP',
    'Education': 'EDU',
    'Research': 'REA',
    'Sports': 'SPO',
    'Sponsored Grant': 'SG',
    'Research Project': 'RP',
    'Consultancy': 'CONS',
    'M.Tech Students Guided': 'M_TECH',
    'Ph.D Students Guided': 'PH_D',
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

if(!csrfToken) {
    window.location.href = "/cookie";
}

checkboxGroup.addEventListener('change', (e) => {
    if (e.target.tagName === 'SELECT') {
        // generateInputFields();
    }
});

checkboxGroup.addEventListener('change', (e) => {
    if (e.target.tagName === 'SELECT') {
        // If checkbox is unchecked, remove its quantity
        if (!e.target.checked) {
            const value = e.target.value;
            delete quantities[value];
        }
        // generateInputFields();\
        const selectedField = document.querySelector('select[name="optradio"]').value;
        currentCategory = selectedField;
        buildForm(currentCategory);

        updateFormCountUI();
        refreshAddFormButtonVisibility();
    }
});

function buildForm(category){

    const subForm = document.createElement('form');
    // const subFormTemplate = document.createElement('template');
    // subFormTemplate.id = 'subFormTemplate';
    subForm.className = 'sub-form needs-validation';
    subForm.setAttribute('novalidate', '');
    subForm.style = 'flex-direction: column';
    subForm.method  = 'POST';
    subForm.enctype = 'multipart/form-data';
    formCounter += 1;
    const i = formCounter;

    subForm.dataset.category = category;

    if(form_number === '1') {
        subForm.innerHTML = `
            <div class="sub-form-title" style = "font-size: 1.5rem; color: #667eea;">
                <b class="sub-form-heading">${category} #${i}</b>
                <button type="button" class="discard-btn" title="Discard this form" aria-label="Discard this form">&times;</button>
            </div>
            <input type = "hidden" name = "csrfmiddlewaretoken" value = "${csrfToken}">
            <input type = "hidden" name = "category" value = "${categoryValue[category]}">
            <div class="sub-form-fields">
                <div class="row g-3">
                    <div class="col-md-4">
                        <div class="row align-items-center">
                            <label for="top-${i}" class="col-sm-4 col-form-label">Title Of the Program<span class="ms-1" style="color: red;">*</span></label>
                            <div class = "col-md-8">
                                <input type="text" class="form-control custom-back" title="Numbers and special characters are not allowed" id="top-${i}" placeholder="Enter title of the program" name="top">
                                <div class="invalid-feedback">Please provide a program title.</div>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-4">
                        <div class="row align-items-center">
                            <label class="col-sm-4 col-form-label ">Mode (Offline/Online)<span class="ms-1" style="color: red;">*</span></label>
                            <div class = "col-sm-8 mb-3">
                                <div class="d-flex column-gap-4">
                                    <div class="form-check">
                                        <input type="radio" class="form-check-input" id="radio1-${i}" name="optradio" value="On" required>
                                        <label class="form-check-label" for="radio1-${i}">Online</label>
                                    </div>
                                    <div class="form-check">
                                        <input type="radio" class="form-check-input" id="radio2-${i}" name="optradio" value="Of">
                                        <label class="form-check-label" for="radio2-${i}">Offline</label>
                                    </div>
                                </div>
                                <div class="invalid-feedback">Please select a mode.</div>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-4">
                        <div class="row align-items-center">
                            <label class="col-sm-4 col-form-label gap-2">Level<span class="ms-1" style="color: red;">*</span></label>
                            <div class="col-sm-8">
                                <div class="d-flex column-gap-4">
                                    <div class="form-check">
                                        <input type="radio" class="form-check-input" id="radio3-${i}" name="optradio1" value="Na" required>
                                        <label class="form-check-label" for="radio3-${i}">National</label>
                                    </div>
                                    <div class="form-check">
                                        <input type="radio" class="form-check-input" id="radio4-${i}" name="optradio1" value="In">
                                        <label class="form-check-label" for="radio4-${i}">International</label>
                                    </div>
                                </div>
                                <div class="invalid-feedback">Please select a level.</div>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-4">
                        <div class="row align-items-center">
                            <label class="col-sm-4 col-form-label">Organizer<span class="ms-1" style="color: red;">*</span><span class="fa-solid fa-circle-info" data-bs-toggle="tooltip" data-bs-placement="top" title="${fieldInfo['Organizer']}"></span></label>
                            <div class="col-sm-8">
                                <input type="text" class="form-control" placeholder="Enter organizer" name = "organizer" required>
                                <div class="invalid-feedback">Please provide an organizer name.</div>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-4">
                        <div class="row align-items-center">
                            <label class="col-sm-4 col-form-label">Sponsored By<span class="ms-1" style="color: red;">*</span><span class="fa-solid fa-circle-info" data-bs-toggle="tooltip" data-bs-placement="top" title="${fieldInfo['Sponsered By']}"></span></label>
                            <div class="col-sm-8">
                                <input type="text" class="form-control" placeholder="Enter sponsors" name = "sponser" required>
                                <div class="invalid-feedback">Please provide sponsor details.</div>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-4">
                        <div class="row align-items-center">
                            <label class="col-sm-4 col-form-label">Grant received from SKIT (Yes/No)<span class="ms-1" style="color: red;">*</span><span class="fa-solid fa-circle-info" data-bs-toggle="tooltip" data-bs-placement="top" title="${fieldInfo['SKIT Approved']}"></span></label>
                            <div class="col-sm-8">
                                <div class="d-flex column-gap-4">
                                    <div class="form-check">
                                        <input type="radio" class="form-check-input" id="radio5-${i}" name="optradio2" value="y" required>
                                        <label class="form-check-label" for="radio5">Yes</label>
                                    </div>
                                    <div class="form-check">
                                        <input type="radio" class="form-check-input" id="radio6-${i}" name="optradio2" value="N">
                                        <label class="form-check-label" for="radio6-${i}">No</label>
                                    </div>
                                </div>
                                <div class="invalid-feedback">Please select approval status.</div>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-4">
                        <div class="row align-items-center">
                            <label class="col-sm-4 col-form-label">From Date<span class="ms-1" style="color: red;">*</span></label>
                            <div class="col-sm-8">
                                <input type="date" class="form-control" name = "begi_date" id = "begi_date" required>
                                <div class="invalid-feedback">Please provide a start date.</div>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-4">
                        <div class="row align-items-center">
                            <label class="col-sm-4 col-form-label">To Date<span class="ms-1" style="color: red;">*</span></label>
                            <div class="col-sm-8">
                                <input type="date" class="form-control" name = "end_date" id = "end_date" required>
                                <div class="invalid-feedback">Please provide an end date.</div>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-4">
                        <div class="row align-items-center">
                            <label class="col-sm-4 col-form-label">Session<span class="ms-1" style="color: red;">*</span><span class="fa-solid fa-circle-info" data-bs-toggle="tooltip" data-bs-placement="top" title="${fieldInfo['Session']}"></span></label>
                            <div class="col-sm-8">
                                <select class="form-select custom-back-select" name="sessionyear" id="sessionyear" required>
                                    <option value="" selected disabled>Select your Session</option>
                                    <option value="2024-25">2024-25</option>
                                    <option value="2025-26">2025-26</option>
                                    <option value="2026-27">2026-27</option>
                                    <option value="2027-28">2027-28</option>
                                    <option value="2028-29">2028-29</option>
                                    <option value="2029-30">2029-30</option>
                                </select>
                                <div class="invalid-feedback">Please select a session.</div>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-4">
                        <div class="row align-items-center">
                            <label class="col-sm-4 col-form-label">No. of days<span class="ms-1" style="color: red;">*</span></label>
                            <div class="col-sm-8">
                                <input type="text" class="form-control" min="0" placeholder="Enter number of days" name = "num_of_days" id = "num_of_days" required>
                                <div class="invalid-feedback">Please provide number of days.</div>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-4">
                        <div class="row align-items-center">
                            <label class="col-sm-4 col-form-label">Proof Enclosed  (Yes/No)<span class="ms-1" style="color: red;">*</span><span class="fa-solid fa-circle-info" data-bs-toggle="tooltip" data-bs-placement="top" title="${fieldInfo['Proof Enclosed']}"></span></label>
                            <div class="col-sm-8">
                                <div class="d-flex column-gap-4">
                                    <div class="form-check">
                                        <input type="radio" class="form-check-input" id="radio7-${i}" name="optradio3" value="y" required>
                                        <label class="form-check-label" for="radio7-${i}">Yes</label>
                                    </div>
                                    <div class="form-check">
                                        <input type="radio" class="form-check-input" id="radio8-${i}" name="optradio3" value="N">
                                        <label class="form-check-label" for="radio8-${i}">No</label>
                                    </div>
                                </div>
                                <div class="invalid-feedback">Please select proof status.</div>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-6">
                        <div class="row align-items-center">
                            <label class="col-sm-4 col-form-label">Upload Certificate/Proof<span class="ms-1" style="color: red;">*</span><span class="fa-solid fa-circle-info" data-bs-toggle="tooltip" data-bs-placement="top" title="${fieldInfo['Upload Certificate/Proof']}"></span>
                            <h5 class="font-small mt-2" style="font-size: 14px; color: gray;">Upload .pdf,.jpg,.jpeg,.png File Format(MAX SIZE:- 2MB)</h5></label>
                            <div class="col-sm-6">
                                <input type="file" class="form-control" placeholder="Upload files" accept=".pdf,.jpg,.jpeg,.png" name="proof_file" required>
                                <div class="invalid-feedback">Please upload a PDF, JPG/JPEG or PNG file only.</div>
                            </div>
                        </div>
                    </div>
                    <div class="subform-actions">
                        <button type="submit" class="btn btn-blue btn-submit">Submit</button>
                        <button type="button" class="btn btn-outline btn-addform">+ Add Form</button>
                    </div>
                </div>
            </div>
            <hr>
        `;
    } else if(form_number === '2') {
        subForm.innerHTML = `
            <div class="sub-form-title" style = "font-size: 1.5rem; color: #667eea;"><b>${category} #${i}</b></div>
            <input type = "hidden" name = "csrfmiddlewaretoken" value = "${csrfToken}">
            <input type = "hidden" name = "category" value = "${categoryValue[category]}">
            <div class="sub-form-fields">
                <div class="row g-3">
                    <div class="col-md-6">
                        <div class="row align-items-center">
                            <label class="col-sm-4 col-form-label">Session<span class="ms-1" style="color: red;">*</span><span class="fa-solid fa-circle-info" data-bs-toggle="tooltip" data-bs-placement="top" title="${fieldInfo['Session']}"></span></label>
                            <div class="col-sm-8">
                                <select class="form-select custom-back-select" name="sessionyear" id="sessionyear" required>
                                    <option value="" selected disabled>Select your Session</option>
                                    <option value="2024-25">2024-25</option>
                                    <option value="2025-26">2025-26</option>
                                    <option value="2026-27">2026-27</option>
                                    <option value="2027-28">2027-28</option>
                                    <option value="2028-29">2028-29</option>
                                    <option value="2029-30">2029-30</option>
                                </select>
                                <div class="invalid-feedback">Please select a session.</div>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-6">
                        <div class="row align-items-center">
                            <label for="toc-${i}" class="col-sm-4 col-form-label">Timeline of course<span class="ms-1" style="color: red;">*</span><span class="fa-solid fa-circle-info" data-bs-toggle="tooltip" data-bs-placement="top" title="${fieldInfo['Timeline of Course']}"></span></label>
                            <div class = "col-md-8">
                                <input type="text" class="form-control" id="toc-${i}" placeholder="Enter timeline of the program" name="toc" required>
                                <div class="invalid-feedback">Please provide timeline of the course.</div>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-6">
                        <div class="row align-items-center">
                            <label class="col-sm-4 col-form-label">Name of the Course<span class="ms-1" style="color: red;">*</span><span class="fa-solid fa-circle-info" data-bs-toggle="tooltip" data-bs-placement="top" title="${fieldInfo['Name of the Course']}"></span></label>
                            <div class="col-sm-8">
                                <input type="text" class="form-control" placeholder="Enter name of course" name = "noc" required>
                                <div class="invalid-feedback">Please provide name of the course.</div>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-6">
                        <div class="row align-items-center">
                            <label class="col-sm-4 col-form-label">Duration of Course<span class="ms-1" style="color: red;">*</span></label>
                            <div class = "col-sm-8">
                                <div class="d-flex column-gap-4">
                                    <div class="form-check">
                                        <input type="radio" class="form-check-input" id="radio1-${i}" name="optradio3" value="4" required>
                                        <label class="form-check-label" for="radio1">4 Week</label>
                                    </div>
                                    <div class="form-check">
                                        <input type="radio" class="form-check-input" id="radio2-${i}" name="optradio3" value="8">
                                        <label class="form-check-label" for="radio2-${i}">8 Week</label>
                                    </div>
                                    <div class="form-check">
                                        <input type="radio" class="form-check-input" id="radio3-${i}" name="optradio3" value="12">
                                        <label class="form-check-label" for="radio3-${i}">12 Week</label>
                                    </div>
                                    <div class="form-check">
                                        <input type="radio" class="form-check-input" id="radio4-${i}" name="optradio3" value="O">
                                        <label class="form-check-label" for="radio4-${i}">Other</label>
                                    </div>
                                </div>
                                <div class="invalid-feedback">Please select duration.</div>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-6">
                        <div class="row align-items-center">
                            <label class="col-sm-4 col-form-label">Start Date of Course<span class="ms-1" style="color: red;">*</span></label>
                            <div class="col-sm-8">
                                <input type="date" class="form-control" name = "begi_date" required>
                                <div class="invalid-feedback">Please provide start date.</div>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-6">
                        <div class="row align-items-center">
                            <label class="col-sm-4 col-form-label">End Date of Course<span class="ms-1" style="color: red;">*</span></label>
                            <div class="col-sm-8">
                                <input type="date" class="form-control" name = "end_date" required>
                                <div class="invalid-feedback">Please provide end date.</div>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-6">
                        <div class="row align-items-center">
                            <label class="col-sm-4 col-form-label">Offering Agency/ Organizer<span class="ms-1" style="color: red;">*</span><span class="fa-solid fa-circle-info" data-bs-toggle="tooltip" data-bs-placement="top" title="${fieldInfo['Offering Agency / Organizer']}"></span></label>
                            <div class="col-sm-8">
                                <input type="text" class="form-control" placeholder="Enter Offering Agency" name = "ofo" required>
                                <div class="invalid-feedback">Please provide offering agency/organizer.</div>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-12">
                        <div class="row align-items-center">
                            <label class="col-sm-4 col-form-label">Certificate Type<span class="ms-1" style="color: red;">*</span></label>
                            <div class="col-sm-8">
                                <div class="d-flex column-gap-4">
                                    <div class="form-check">
                                        <input type="radio" class="form-check-input" id="radio5-${i}" name="optradio1" value="G" required>
                                        <label class="form-check-label" for="radio5">Gold</label>
                                    </div>
                                    <div class="form-check">
                                        <input type="radio" class="form-check-input" id="radio6-${i}" name="optradio1" value="S">
                                        <label class="form-check-label" for="radio6-${i}">Silver</label>
                                    </div>
                                    <div class="form-check">
                                        <input type="radio" class="form-check-input" id="radio7-${i}" name="optradio1" value="E">
                                        <label class="form-check-label" for="radio7">Elite</label>
                                    </div>
                                    <div class="form-check">
                                        <input type="radio" class="form-check-input" id="radio8-${i}" name="optradio1" value="SC">
                                        <label class="form-check-label" for="radio8-${i}">Successfully Completed</label>
                                    </div>

                                </div>
                                <div class="invalid-feedback">Please select certificate type.</div>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-12">
                        <div class="row align-items-center">
                            <label class="col-sm-4 col-form-label">Any category from below<span class="ms-1" style="color: red;">*</span></label>
                            <div class="col-sm-8">
                                <div class="d-flex column-gap-4">
                                    <div class="form-check">
                                        <input type="radio" class="form-check-input" id="radio9-${i}" name="optradio2" value="1" required>
                                        <label class="form-check-label" for="radio9">Topper of 1% in this course</label>
                                    </div>
                                    <div class="form-check">
                                        <input type="radio" class="form-check-input" id="radio10-${i}" name="optradio2" value="2">
                                        <label class="form-check-label" for="radio10-${i}">Topper of 2% in this course</label>
                                    </div>
                                    <div class="form-check">
                                        <input type="radio" class="form-check-input" id="radio11-${i}" name="optradio2" value="5">
                                        <label class="form-check-label" for="radio11-${i}">Topper of 5% in this course</label>
                                    </div>
                                    <div class="form-check">
                                        <input type="radio" class="form-check-input" id="radio12-${i}" name="optradio2" value="10">
                                        <label class="form-check-label" for="radio12-${i}">Topper of 10% in this course</label>
                                    </div>
                                    <div class="form-check">
                                        <input type="radio" class="form-check-input" id="radio13-${i}" name="optradio2" value="NA">
                                        <label class="form-check-label" for="radio13">Not Applicable</label>
                                    </div>
                                </div>
                                <div class="invalid-feedback">Please select a category.</div>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-6">
                        <div class="row align-items-center">
                            <label class="col-sm-4 col-form-label">Upload Certificate<span class="ms-1" style="color: red;">*</span><span class="fa-solid fa-circle-info" data-bs-toggle="tooltip" data-bs-placement="top" title="${fieldInfo['Upload Certificate(MOOC)']}"></span>
                            <h5 class="font-small mt-2" style="font-size: 14px; color: gray;">Upload .pdf,.jpg,.jpeg,.png File Format(MAX SIZE:- 2MB)</h5></label>
                            <div class="col-sm-6">
                                <input type="file" class="form-control" placeholder="Upload files" accept=".pdf,.jpg,.jpeg,.png" name="proof_file" required>
                                <div class="invalid-feedback">Please upload a PDF, JPG/JPEG or PNG file only.</div>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-6">
                        <div class="row align-items-center">
                            <label class="col-sm-4 col-form-label">Remarks(If any)</label>
                            <div class="col-sm-8">
                                <input type="text" class="form-control" placeholder="Enter Remarks" name = "remarks">
                                <div class="invalid-feedback">Please provide remarks.</div>
                            </div>
                        </div>
                    </div>
                    <div class="subform-actions">
      <button type="button" class="btn btn-blue btn-submit">Submit</button>
      <button type="button" class="btn btn-outline btn-addform">+ Add Form</button>
    </div>
                </div>
            </div>
            <hr>
        `;
    } else if (form_number === '3') {
        subForm.innerHTML = `
            <div class="sub-form-title" style = "font-size: 1.5rem; color: #667eea;"><b>${category} #${i}</b></div>
            <input type = "hidden" name = "csrfmiddlewaretoken" value = "${csrfToken}">
            <input type = "hidden" name = "category" value = "${categoryValue[category]}">
            <div class="sub-form-fields">
                <div class="row g-3">
                    <div class="col-md-6">
                        <div class="row align-items-center">
                            <label class="col-sm-4 col-form-label">Start Date of the Event<span class="ms-1" style="color: red;">*</span></label>
                            <div class="col-sm-8">
                                <input type="date" class="form-control" name = "begi_date" required>
                                <div class="invalid-feedback">Please provide the start date of the event.</div>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-6">
                        <div class="row align-items-center">
                            <label class="col-sm-4 col-form-label">End Date of the Event<span class="ms-1" style="color: red;">*</span></label>
                            <div class="col-sm-8">
                                <input type="date" class="form-control" name = "end_date" required>
                                <div class="invalid-feedback">Please provide the end date of the event.</div>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-6">
                        <div class="row align-items-center">
                            <label class="col-sm-4 col-form-label">Event organized for<span class="ms-1" style="color: red;">*</span></label>
                            <div class="col-sm-8 mt-4">
                                <div class="d-flex column-gap-4">
                                    <div class="form-check">
                                        <input type="checkbox" class="form-check-input group-required" id="radio1-${i}" name="optradio3" value="S">
                                        <label class="form-check-label" for="radio1">Students</label>
                                    </div>
                                    <div class="form-check">
                                        <input type="checkbox" class="form-check-input" id="radio2-${i}" name="optradio3" value="TS">
                                        <label class="form-check-label" for="radio2-${i}">Teaching Staff</label>
                                    </div>
                                    <div class="form-check">
                                        <input type="checkbox" class="form-check-input" id="radio3-${i}" name="optradio3" value="NTS">
                                        <label class="form-check-label" for="radio3">Non-Teaching Staff</label>
                                    </div>
                                </div>
                                <div class="invalid-feedback">Please select at least one option.</div>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-6">
                        <div class="row align-items-center">
                            <label class="col-sm-4 col-form-label">Name of Faculty Coordinator(s)<span class="ms-1" style="color: red;">*</span></label>
                            <div class = "col-sm-8">
                                <input type="text" class="form-control" placeholder="Enter Name of Faculty Coordinator(s)" name = "nofc" required>
                                <div class="invalid-feedback">Please provide the title of the program.</div>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-6">
                        <div class="row align-items-center">
                            <label class="col-sm-4 col-form-label">Title of the Professional Development Program Organized<span class="ms-1" style="color: red;">*</span><span class="fa-solid fa-circle-info" data-bs-toggle="tooltip" data-bs-placement="top" title="${fieldInfo['Title of the Professional Development Program Organized']}"></span></label>
                            <div class = "col-sm-8">
                                <input type="text" class="form-control" placeholder="Enter title of the Professional Development Program Organized" name = "topdpo" required>
                                <div class="invalid-feedback">Please provide the title of the program.</div>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-6" style = "margin-top: 4rem;">
                        <div class="row align-items-center">
                            <label class="col-sm-4 col-form-label">No. of participants<span class="ms-1" style="color: red;">*</span></label>
                            <div class = "col-sm-8">
                                <input type="number" class="form-control" placeholder="Enter no. of participants" name = "nop" required>
                                <div class="invalid-feedback">Please provide number of participants.</div>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-6">
                        <div class="row align-items-center">
                            <label class="col-sm-4 col-form-label">Academic Department/ Cell/ Committees/ Labs/ COE<span class="ms-1" style="color: red;">*</span><span class="fa-solid fa-circle-info" data-bs-toggle="tooltip" data-bs-placement="top" title="${fieldInfo['Academic Department/ Cell / Committees/ Labs /COE']}"></span></label>
                            <div class = "col-sm-8">
                                <input type="text" class="form-control" placeholder="Enter Academic Department/ Cell/ Committees/ Labs/ COE" name = "adcc" required>
                                <div class="invalid-feedback">Please provide the department/cell/committee/lab/COE.</div>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-6 mt-5">
                        <div class="row align-items-center">
                            <label class="col-sm-4 col-form-label">Academic Session<span class="ms-1" style="color: red;">*</span><span class="fa-solid fa-circle-info" data-bs-toggle="tooltip" data-bs-placement="top" title="${fieldInfo['Session']}"></span></label>
                            <div class="col-sm-8">
                                <select class="form-select custom-back-select" name="sessionyear" id="sessionyear" required>
                                    <option value="" selected disabled>Select your Session</option>
                                    <option value="2024-25">2024-25</option>
                                    <option value="2025-26">2025-26</option>
                                    <option value="2026-27">2026-27</option>
                                    <option value="2027-28">2027-28</option>
                                    <option value="2028-29">2028-29</option>
                                    <option value="2029-30">2029-30</option>
                                </select>
                                <div class="invalid-feedback">Please select a session.</div>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-6">
                        <div class="row align-items-center">
                            <label class="col-sm-4 col-form-label">Sponsored/Non Sponsored<span class="ms-1" style="color: red;">*</span></label>
                            <div class="col-sm-8">
                                <div class="d-flex column-gap-4">
                                    <div class="form-check">
                                        <input type="radio" class="form-check-input" id="radio3-${i}" name="optradio1" value="S" required>
                                        <label class="form-check-label" for="radio3">Sponsored</label>
                                    </div>
                                    <div class="form-check">
                                        <input type="radio" class="form-check-input" id="radio4-${i}" name="optradio1" value="NS">
                                        <label class="form-check-label" for="radio4-${i}">Non-Sponsored</label>
                                    </div>
                                </div>
                                <div class="invalid-feedback">Please select certificate type.</div>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-6">
                        <div class="row align-items-center">
                            <label class="col-sm-4 col-form-label">Name of Sponsoring Agency(if Sponsored)<span class="ms-1" style="color: red;">*</span><span class="fa-solid fa-circle-info" data-bs-toggle="tooltip" data-bs-placement="top" title="${fieldInfo['Not Applicable']}"></span></label>
                            <div class = "col-sm-8">
                                <input type="text" class="form-control" placeholder="Enter name of sponsoring agency" name = "nosa" required>
                                <div class="invalid-feedback">Please provide name of sponsoring agency.</div>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-6">
                        <div class="row align-items-center">
                            <label class="col-sm-4 col-form-label">Collaboration Details<span class="ms-1" style="color: red;">*</span><span class="fa-solid fa-circle-info" data-bs-toggle="tooltip" data-bs-placement="top" title="${fieldInfo['Collaboration Details']}"></span></label>
                            <div class = "col-sm-8">
                                <input type="text" class="form-control" placeholder="Enter collaboration details" name = "cd" required>
                                <div class="invalid-feedback">Please provide collaboration details.</div>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-6">
                        <div class="row align-items-center">
                            <label class="col-sm-4 col-form-label">Grant Received(YES/NO)<span class="ms-1" style="color: red;">*</span><span class="fa-solid fa-circle-info" data-bs-toggle="tooltip" data-bs-placement="top" title="${fieldInfo['SKIT Approved']}"></span></label>
                            <div class="col-sm-8">
                                <div class="d-flex column-gap-4">
                                    <div class="form-check">
                                        <input type="radio" class="form-check-input" id="radio5-${i}" name="optradio2" value="y" required>
                                        <label class="form-check-label" for="radio5">Yes</label>
                                    </div>
                                    <div class="form-check">
                                        <input type="radio" class="form-check-input" id="radio6-${i}" name="optradio2" value="N">
                                        <label class="form-check-label" for="radio6-${i}">No</label>
                                    </div>
                                </div>
                                <div class="invalid-feedback">Please select grant received status.</div>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-6">
                        <div class="row align-items-center">
                            <label class="col-sm-4 col-form-label">Grant Details<span class="ms-1" style="color: red;">*</span><span class="fa-solid fa-circle-info" data-bs-toggle="tooltip" data-bs-placement="top" title="${fieldInfo['Grant Details']}"></label>
                            <div class = "col-sm-8">
                                <input type="text" class="form-control" placeholder="Enter grant details" name = "gd" required>
                                <div class="invalid-feedback">Please provide grant details.</div>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-6">
                        <div class="row align-items-center">
                            <label class="col-sm-4 col-form-label">Actual Expenditure<span class="ms-1" style="color: red;">*</span><span class="fa-solid fa-circle-info" data-bs-toggle="tooltip" data-bs-placement="top" title="e.g : 30000"></label>
                            <div class = "col-sm-8">
                                <input type="number" class="form-control" placeholder="Only write amount (for e.g:- 30000)(evaluated in Rs.)" name = "actual_expenditure" required>
                                <div class="invalid-feedback">Please provide actual expenditure.</div>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-6">
                        <div class="row align-items-center">
                            <label class="col-sm-4 col-form-label">Association with professional societies for organization of event<span class="ms-1" style="color: red;">*</span><span class="fa-solid fa-circle-info" data-bs-toggle="tooltip" data-bs-placement="top" title="${fieldInfo['Association with professional societies for organization of event']}"></span></label>
                            <div class="col-sm-8">
                                <input type="text" class="form-control" placeholder="Enter details" name = "awpsfooe" required>
                                <div class="invalid-feedback">Please provide association details.</div>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-6">
                        <div class="row align-items-center">
                            <label class="col-sm-4 col-form-label">Number of SKIT students participated (Provide list of students with their RTU roll no. & Certificates)<span class="ms-1" style="color: red;">*</span><span class="fa-solid fa-circle-info" data-bs-toggle="tooltip" data-bs-placement="top" title="${fieldInfo['Not Applicable']}"></span></label>
                            <div class="col-sm-8">
                                <input type="text" class="form-control" placeholder="Enter details" name = "nossp" required>
                                <div class="invalid-feedback">Please provide number of SKIT students participated.</div>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-6">
                        <div class="row align-items-center">
                            <label class="col-sm-4 col-form-label">Number of staff member participated(Provide list of staff members with  their EMPLOYEE ID & Certificates)<span class="ms-1" style="color: red;">*</span><span class="fa-solid fa-circle-info" data-bs-toggle="tooltip" data-bs-placement="top" title="${fieldInfo['Not Applicable']}"></span></label>
                            <div class="col-sm-8">
                                <input type="text" class="form-control" placeholder="Enter details" name = "nosmp" required>
                                <div class="invalid-feedback">Please provide number of staff members participated.</div>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-12">
                        <div class="row align-items-center">
                            <label class="col-sm-2 col-form-label">Mapped SDG's<span class="ms-1" style="color: red;">*</span><span class="fa-solid fa-circle-info" data-bs-toggle="tooltip" data-bs-placement="top" title="${fieldInfo['Mapped SDGs']}"></label>
                            <div class = "col-sm-10 mt-4">
                                <div class="d-flex column-gap-4">
                                    <div class="form-check">
                                        <input type="checkbox" class="form-check-input group-required" id="radio1-${i}" name="optradio4" value="SDG1">
                                        <label class="form-check-label" for="radio1">SDG - 1 (No Poverty)</label>
                                    </div>
                                    <div class="form-check">
                                        <input type="checkbox" class="form-check-input" id="radio2-${i}" name="optradio4" value="SDG2">
                                        <label class="form-check-label" for="radio2-${i}">SDG - 2 (Zero Hunger)</label>
                                    </div>
                                    <div class="form-check">
                                        <input type="checkbox" class="form-check-input" id="radio3-${i}" name="optradio4" value="SDG3">
                                        <label class="form-check-label" for="radio3">SDG - 3 (Good Health And Well-Being)</label>
                                    </div>
                                    <div class="form-check">
                                        <input type="checkbox" class="form-check-input" id="radio4-${i}" name="optradio4" value="SDG4">
                                        <label class="form-check-label" for="radio3">SDG - 4 (Quality Education)</label>
                                    </div>
                                    <div class="form-check">
                                        <input type="checkbox" class="form-check-input" id="radio5-${i}" name="optradio4" value="SDG5">
                                        <label class="form-check-label" for="radio3">SDG - 5 (Gender Equality)</label>
                                    </div>
                                    <div class="form-check">
                                        <input type="checkbox" class="form-check-input" id="radio6-${i}" name="optradio4" value="SDG6">
                                        <label class="form-check-label" for="radio3">SDG - 6 (Clean Water And Sanitation)</label>
                                    </div>
                                    <div class="form-check">
                                        <input type="checkbox" class="form-check-input" id="radio7-${i}" name="optradio4" value="SDG7">
                                        <label class="form-check-label" for="radio3">SDG - 7 (Affordable And Clean Energy)</label>
                                    </div>
                                    <div class="form-check">
                                        <input type="checkbox" class="form-check-input" id="radio8-${i}" name="optradio4" value="SDG8">
                                        <label class="form-check-label" for="radio3">SDG - 8 (Decent Work And Economic Growth)</label>
                                    </div>
                                    <div class="form-check">
                                        <input type="checkbox" class="form-check-input" id="radio9-${i}" name="optradio4" value="SDG9">
                                        <label class="form-check-label" for="radio3">SDG - 9 (Industry, Innovation And Infrastructure)</label>
                                    </div>
                                </div>
                                <div class="d-flex column-gap-4">    
                                    <div class="form-check">
                                        <input type="checkbox" class="form-check-input" id="radio10-${i}" name="optradio4" value="SDG10">
                                        <label class="form-check-label" for="radio3">SDG - 10 (Reduced Inequalities)</label>
                                    </div>
                                    <div class="form-check">
                                        <input type="checkbox" class="form-check-input" id="radio11-${i}" name="optradio4" value="SDG11">
                                        <label class="form-check-label" for="radio3">SDG - 11 (Sustainable Cities And Communities)</label>
                                    </div>
                                    <div class="form-check">
                                        <input type="checkbox" class="form-check-input" id="radio12-${i}" name="optradio4" value="SDG12">
                                        <label class="form-check-label" for="radio3">SDG - 12 (Responsible Consumption And Production)</label>
                                    </div>
                                    <div class="form-check">
                                        <input type="checkbox" class="form-check-input" id="radio13-${i}" name="optradio4" value="SDG13">
                                        <label class="form-check-label" for="radio3">SDG - 13 (Climate Action)</label>
                                    </div>
                                    <div class="form-check">
                                        <input type="checkbox" class="form-check-input" id="radio14-${i}" name="optradio4" value="SDG14">
                                        <label class="form-check-label" for="radio3">SDG - 14 (Life Below Water)</label>
                                    </div>
                                    <div class="form-check">
                                        <input type="checkbox" class="form-check-input" id="radio15-${i}" name="optradio4" value="SDG15">
                                        <label class="form-check-label" for="radio3">SDG - 15 (Life On Land)</label>
                                    </div>
                                    <div class="form-check">
                                        <input type="checkbox" class="form-check-input" id="radio16-${i}" name="optradio4" value="SDG16">
                                        <label class="form-check-label" for="radio3">SDG - 16 (Peace, Justice, And Strong Institutions)</label>
                                    </div>
                                    <div class="form-check">
                                        <input type="checkbox" class="form-check-input" id="radio17-${i}" name="optradio4" value="SDG17">
                                        <label class="form-check-label" for="radio3">SDG - 17 (Partnerships For The Goals)</label>
                                    </div>
                                </div>
                                <div class="invalid-feedback">Please select at least one option.</div>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-4">
                        <div class="row align-items-center">
                            <label class="col-sm-4 col-form-label">Event report attached in proper format(YES/NO)<span class="ms-1" style="color: red;">*</span><span class="fa-solid fa-circle-info" data-bs-toggle="tooltip" data-bs-placement="top" title="${fieldInfo['Event report attached in proper format']}"></span></label>
                            <div class="col-sm-8">
                                <div class="d-flex column-gap-4">
                                    <div class="form-check">
                                        <input type="radio" class="form-check-input" id="radio5-${i}-${i}" name="optradio5" value="y" required>
                                        <label class="form-check-label" for="radio5">Yes</label>
                                    </div>
                                    <div class="form-check">
                                        <input type="radio" class="form-check-input" id="radio6-${i}" name="optradio5" value="N">
                                        <label class="form-check-label" for="radio6-${i}">No</label>
                                    </div>
                                </div>
                                <div class="invalid-feedback">Please select an option.</div>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-6">
                        <div class="row align-items-center">
                            <label class="col-sm-4 col-form-label">Upload Event Report<span class="ms-1" style="color: red;">*</span><span class="fa-solid fa-circle-info" data-bs-toggle="tooltip" data-bs-placement="top" title="${fieldInfo['Upload Event Report']}"></span>
                            <h5 class="font-small mt-2" style="font-size: 14px; color: gray;">Upload .pdf,.jpg,.jpeg,.png File Format(MAX SIZE:- 2MB)</h5></label>
                            <div class="col-sm-6">
                                <input type="file" class="form-control" placeholder="Upload files" accept=".pdf,.jpg,.jpeg,.png" name="proof_file" required>
                                <div class="invalid-feedback">Please upload a PDF, JPG/JPEG or PNG file only.</div>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-6">
                        <div class="row align-items-center">
                            <label class="col-sm-4 col-form-label">Any Other Remark(If any)</label>
                            <div class="col-sm-8">
                                <input type="text" class="form-control" placeholder="Enter Remarks" name = "remarks">
                                <div class="invalid-feedback">Please provide remarks.</div>
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
    } else if(form_number === '4') {
        subForm.innerHTML = `
            <div class="sub-form-title" style = "font-size: 1.5rem; color: #667eea;"><b>${category} #${i}</b></div>
            <input type = "hidden" name = "category" value = "${categoryValue[category]}">
            <input type = "hidden" name = "csrfmiddlewaretoken" value = "${csrfToken}">
            <div class="sub-form-fields">
                <div class="row g-3">
                    <div class="col-md-4" style = "margin-top: 2.5rem;">
                        <div class="row align-items-center">
                            <label class="col-sm-4 col-form-label">Session<span class="ms-1" style="color: red;">*</span><span class="fa-solid fa-circle-info" data-bs-toggle="tooltip" data-bs-placement="top" title="${fieldInfo['Session']}"></span></label>
                            <div class="col-sm-8">
                                <select class="form-select custom-back-select" name="sessionyear" id="sessionyear" required>
                                    <option value="" selected disabled>Select your Session</option>
                                    <option value="2024-25">2024-25</option>
                                    <option value="2025-26">2025-26</option>
                                    <option value="2026-27">2026-27</option>
                                    <option value="2027-28">2027-28</option>
                                    <option value="2028-29">2028-29</option>
                                    <option value="2029-30">2029-30</option>
                                </select>
                                <div class="invalid-feedback">Please select an option.</div>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-4">
                        <div class="row align-items-center">
                            <label for="top" class="col-sm-4 col-form-label">Name of the Award/   Achievement<span class="ms-1" style="color: red;">*</span><span class="fa-solid fa-circle-info" data-bs-toggle="tooltip" data-bs-placement="top" title="${fieldInfo['Name of the Award/Achievement']}"></span></label>
                            <div class = "col-md-8">
                                <input type="text" class="form-control custom-back" id="top" placeholder="Enter name of award / achievement" name="noaa" required>
                                <div class="invalid-feedback">Please provide name of award / achievement.</div>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-4">
                        <div class="row align-items-center">
                            <label class="col-sm-4 col-form-label">Position / Award For<span class="ms-1" style="color: red;">*</span><span class="fa-solid fa-circle-info" data-bs-toggle="tooltip" data-bs-placement="top" title="${fieldInfo['Position / Award For']}"></span></label>
                            <div class="col-sm-8">
                                <input type="text" class="form-control" placeholder="Enter award for" name = "paf" required>
                                <div class="invalid-feedback">Please provide position / award for.</div>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-4">
                        <div class="row align-items-center">
                            <label class="col-sm-4 col-form-label">Agency / Organization<span class="ms-1" style="color: red;">*</span><span class="fa-solid fa-circle-info" data-bs-toggle="tooltip" data-bs-placement="top" title="${fieldInfo['Agency / Organization']}"></span></label>
                            <div class="col-sm-8">
                                <input type="text" class="form-control" placeholder="Enter organizer" name = "ao" required>
                                <div class="invalid-feedback">Please provide agency / organization.</div>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-4">
                        <div class="row align-items-center">
                            <label class="col-sm-4 col-form-label">Prize<span class="ms-1" style="color: red;">*</span><span class="fa-solid fa-circle-info" data-bs-toggle="tooltip" data-bs-placement="top" title="${fieldInfo['Prize']}"></span></label>
                            <div class="col-sm-8">
                                <input type="text" class="form-control" placeholder="Enter organizer" name = "prize" required>
                                <div class="invalid-feedback">Please provide prize.</div>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-4">
                        <div class="row align-items-center">
                            <label class="col-sm-4 col-form-label">Date of Award<span class="ms-1" style="color: red;">*</span></label>
                            <div class="col-sm-8">
                                <input type="date" class="form-control" name = "award_date" required>
                                <div class="invalid-feedback">Please provide award date.</div>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-6">
                        <div class="row align-items-center">
                            <label class="col-sm-4 col-form-label">Upload Award Certificate/Proof<span class="ms-1" style="color: red;">*</span><span class="fa-solid fa-circle-info" data-bs-toggle="tooltip" data-bs-placement="top" title="${fieldInfo['Upload Award Certificate/Proof']}"></span>
                            <h5 class="font-small mt-2" style="font-size: 14px; color: gray;">Upload .pdf,.jpg,.jpeg,.png File Format(MAX SIZE:- 2MB)</h5></label>
                            <div class="col-sm-6">
                                <input type="file" class="form-control" placeholder="Upload files" accept=".pdf,.jpg,.jpeg,.png" name="proof_file" required>
                                <div class="invalid-feedback">Please upload a PDF, JPG/JPEG or PNG file only.</div>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-4">
                        <div class="row align-items-center">
                            <label class="col-sm-4 col-form-label">Remark<span class="fa-solid fa-circle-info" data-bs-toggle="tooltip" data-bs-placement="top" title="${fieldInfo['Remark']}"></span></label>
                            <div class="col-sm-8">
                                <input type="text" class="form-control" placeholder="Enter organizer" name = "remark">
                                <div class="invalid-feedback">Please provide remark.</div>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-12">
                        <div class="row align-items-center">
                            <label class="col-sm-8 col-form-label">All information filled by me is correct and I will submit proof and other related document whenever is asked<span class="ms-1" style="color: red;">*</span></label>
                            <div class="col-sm-4">
                                <input type="checkbox" class="form-check-input" name = "num_of_days" required>
                                <div class="invalid-feedback">Please confirm the information.</div>
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
    } else if (form_number === '5') {
        subForm.innerHTML = `
            <div class="sub-form-title" style = "font-size: 1.5rem; color: #667eea;"><b>${category} #${i}</b></div>
            <input type = "hidden" name = "category" value = "${categoryValue[category]}">
            <input type = "hidden" name = "csrfmiddlewaretoken" value = "${csrfToken}">
            <div class="sub-form-fields">
                <div class="row g-3">
                    <div class="col-md-4">
                        <div class="row align-items-center">
                            <label for="top" class="col-sm-4 col-form-label">Name of the Funding Agency (MSME/DST/CSIR/SERB /Industry etc.)</label>
                            <div class = "col-md-8">
                                <input type="text" class="form-control custom-back" id="nofa" placeholder="Enter Name of Funding Agency" name="nofa" required>
                                <div class="invalid-feedback">Please provide the name of the funding agency.</div>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-4">
                        <div class="row align-items-center">
                            <label class="col-sm-4 col-form-label">Duration of Project (in Years)<span class="ms-1" style="color: red;">*</span></label>
                            <div class="col-sm-8">
                                <input type="number" class="form-control" placeholder="Enter Duration" name = "dop" required>
                                <div class="invalid-feedback">Please provide duration of project.</div>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-4">
                        <div class="row align-items-center">
                            <label class="col-sm-4 col-form-label">Amount in Rs.<span class="ms-1" style="color: red;">*</span></label>
                            <div class="col-sm-8">
                                <input type="number" class="form-control" placeholder="Enter Amount" name = "amount" required>
                                <div class="invalid-feedback">Please provide amount in Rs.</div>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-4">
                        <div class="row align-items-center">
                            <label class="col-sm-4 col-form-label">Session in which grant/research project/consultancy received<span class="ms-1" style="color: red;">*</span><span class="fa-solid fa-circle-info" data-bs-toggle="tooltip" data-bs-placement="top" title="${fieldInfo['Session']}"></span></label>
                            <div class="col-sm-8">
                                <select class="form-select custom-back-select" name="sessionyear" id="sessionyear" required>
                                    <option value="" selected disabled>Select your Session</option>
                                    <option value="2024-25">2024-25</option>
                                    <option value="2025-26">2025-26</option>
                                    <option value="2026-27">2026-27</option>
                                    <option value="2027-28">2027-28</option>
                                    <option value="2028-29">2028-29</option>
                                    <option value="2029-30">2029-30</option>
                                </select>
                                <div class="invalid-feedback">Please select an option.</div>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-4">
                        <div class="row align-items-center">
                            <label class="col-sm-4 col-form-label">Status<span class="ms-1" style="color: red;">*</span></label>
                            <div class="col-sm-8">
                                <div class="d-flex column-gap-4">
                                    <div class="form-check">
                                        <input type="radio" class="form-check-input" id="radio5-${i}" name="optradio2" value="ON" required>
                                        <label class="form-check-label" for="radio5-${i}">Ongoing</label>
                                    </div>
                                    <div class="form-check">
                                        <input type="radio" class="form-check-input" id="radio6-${i}" name="optradio2" value="CM">
                                        <label class="form-check-label" for="radio6-${i}">Completed</label>
                                    </div>
                                </div>
                                <div class="invalid-feedback">Please select status.</div>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-6">
                        <div class="row align-items-center">
                            <label class="col-sm-4 col-form-label">Upload Proof<span class="ms-1" style="color: red;">*</span><span class="fa-solid fa-circle-info" data-bs-toggle="tooltip" data-bs-placement="top" title="${fieldInfo['Upload Proof']}"></span>
                            <h5 class="font-small mt-2" style="font-size: 14px; color: gray;">Upload .pdf,.jpg,.jpeg,.png File Format(MAX SIZE:- 2MB)</h5></label>
                            <div class="col-sm-6">
                                <input type="file" class="form-control" placeholder="Upload files" accept=".pdf,.jpg,.jpeg,.png" name="proof_file" required>
                                <div class="invalid-feedback">Please upload a PDF, JPG/JPEG or PNG file only.</div>
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
    } else if(form_number === '6') {
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
                                <div class="invalid-feedback">Please provide name of author(s).</div>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-4">
                        <div class="row align-items-center">
                            <label class="col-sm-4 col-form-label">Title of Paper<span class="ms-1" style="color: red;">*</span></label>
                            <div class = "col-sm-8">
                                <input type="text" class="form-control" placeholder="Enter title of Paper" name = "top" required>
                                <div class="invalid-feedback">Please provide title of paper.</div>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-4">
                        <div class="row align-items-center">
                            <label class="col-sm-4 col-form-label">Name of Journal<span class="ms-1" style="color: red;">*</span></label>
                            <div class = "col-sm-8">
                                <input type="text" class="form-control" placeholder="Enter name of journal" name = "noj" required>
                                <div class="invalid-feedback">Please provide name of journal.</div>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-4">
                        <div class="row align-items-center">
                            <label class="col-sm-4 col-form-label">Name of the Publisher<span class="ms-1" style="color: red;">*</span></label>
                            <div class = "col-sm-8">
                                <input type="text" class="form-control"  placeholder="Enter name of publisher" name = "nop" required>
                                <div class="invalid-feedback">Please provide name of publisher.</div>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-4">
                        <div class="row align-items-center">
                            <label class="col-sm-4 col-form-label">Volume, Issue<span class="ms-1" style="color: red;">*</span></label>
                            <div class = "col-sm-8">
                                <input type="text" class="form-control" placeholder="Enter volumne, issue" name = "vi" required>
                                <div class="invalid-feedback">Please provide volume, issue.</div>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-4">
                        <div class="row align-items-center">
                            <label class="col-sm-4 col-form-label">Page No.<span class="ms-1" style="color: red;">*</span></label>
                            <div class = "col-sm-8">
                                <input type="text" class="form-control" placeholder="Enter page no." name = "pn" required>
                                <div class="invalid-feedback">Please provide page no.</div>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-4">
                        <div class="row align-items-center">
                            <label class="col-sm-4 col-form-label">Published Date<span class="ms-1" style="color: red;">*</span></label>
                            <div class="col-sm-8">
                                <input type="date" class="form-control" name = "begi_date" required>
                                <div class="invalid-feedback">Please provide published date.</div>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-4">
                        <div class="row align-items-center">
                            <label class="col-sm-4 col-form-label">Session<span class="ms-1" style="color: red;">*</span><span class="fa-solid fa-circle-info" data-bs-toggle="tooltip" data-bs-placement="top" title="${fieldInfo['Session']}"></span></label>
                            <div class="col-sm-8">
                                <select class="form-select custom-back-select" name="sessionyear" id="sessionyear" required>
                                    <option value="" selected disabled>Select your Session</option>
                                    <option value="2024-25">2024-25</option>
                                    <option value="2025-26">2025-26</option>
                                    <option value="2026-27">2026-27</option>
                                    <option value="2027-28">2027-28</option>
                                    <option value="2028-29">2028-29</option>
                                    <option value="2029-30">2029-30</option>
                                </select>
                                <div class="invalid-feedback">Please select academic session.</div>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-4">
                        <div class="row align-items-center">
                            <label class="col-sm-4 col-form-label">ISSN number : Print<span class="ms-1" style="color: red;">*</span><span class="fa-solid fa-circle-info" data-bs-toggle="tooltip" data-bs-placement="top" title="${fieldInfo['Not Applicable']}"></span></label>
                            <div class = "col-sm-8">
                                <input type="text" class="form-control" placeholder="Enter ISSN number: Print" name = "isnp" required>
                                <div class="invalid-feedback">Please provide ISSN number : Print.</div>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-4">
                        <div class="row align-items-center">
                            <label class="col-sm-4 col-form-label">ISSN number : Online<span class="ms-1" style="color: red;">*</span><span class="fa-solid fa-circle-info" data-bs-toggle="tooltip" data-bs-placement="top" title="${fieldInfo['Not Applicable']}"></span></label>
                            <div class = "col-sm-8">
                                <input type="text" class="form-control" placeholder="Enter ISSN number: online" name = "isno" required>
                                <div class="invalid-feedback">Please provide ISSN number : Online.</div>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-4">
                        <div class="row align-items-center">
                            <label class="col-sm-4 col-form-label">Level (National/ International)<span class="ms-1" style="color: red;">*</span></label>
                            <div class="col-sm-8">
                                <div class="d-flex column-gap-4">
                                    <div class="form-check">
                                        <input type="radio" class="form-check-input" id="radio1-${i}" name="optradio3" value="Na" required>
                                        <label class="form-check-label" for="radio1-${i}">National</label>
                                    </div>
                                    <div class="form-check">
                                        <input type="radio" class="form-check-input" id="radio2-${i}" name="optradio3" value="In">
                                        <label class="form-check-label" for="radio2-${i}">International</label>
                                    </div>
                                </div>
                                <div class="invalid-feedback">Please select level.</div>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-4">
                        <div class="row align-items-center">
                            <label class="col-sm-4 col-form-label">DOI(Digital Object Identifier)<span class="ms-1" style="color: red;">*</span><span class="fa-solid fa-circle-info" data-bs-toggle="tooltip" data-bs-placement="top" title="${fieldInfo['DOI']}"></span></label>
                            <div class = "col-sm-8">
                                <input type="text" class="form-control" placeholder="Enter DOI(Digital Object Identifier)" name = "doi" required>
                                <div class="invalid-feedback">Please provide DOI(Digital Object Identifier).</div>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-4">
                        <div class="row align-items-center">
                            <label class="col-sm-4 col-form-label">Link to website of the Journal<span class="ms-1" style="color: red;">*</span><span class="fa-solid fa-circle-info" data-bs-toggle="tooltip" data-bs-placement="top" title="${fieldInfo['Link to website of the Journal']}"></span></label>
                            <div class = "col-sm-8">
                                <input type="text" class="form-control" placeholder="Enter Link to website of the Journal" name = "lwj" required>
                                <div class="invalid-feedback">Please provide Link to website of the Journal starting with www., http://, or https://. or write na</div>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-4">
                        <div class="row align-items-center">
                            <label class="col-sm-4 col-form-label">Link to article/paper/ abstract of the article<span class="ms-1" style="color: red;">*</span><span class="fa-solid fa-circle-info" data-bs-toggle="tooltip" data-bs-placement="top" title="${fieldInfo['Link to article/paper/abstract of the article']}"></span></label>
                            <div class = "col-sm-8">
                                <input type="text" class="form-control" placeholder="Enter Link to article/paper/abstract of the article " name = "lap" required>
                                <div class="invalid-feedback">Please provide Link to article/paper/ abstract of the article starting with www., http://, or https://.</div>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-4">
                        <div class="row align-items-center">
                            <label class="col-sm-4 col-form-label">Link to the recognition in SCOPUS enlistment of the Journal<span class="ms-1" style="color: red;">*</span></label>
                            <div class = "col-sm-8">
                                <input type="text" class="form-control" placeholder="Enter Link to the recognition in SCOPUS enlistment of the Journal" name = "lrsj" required>
                                <div class="invalid-feedback">Please provide Link to the recognition in SCOPUS enlistment of the Journal starting with www., http://, or https://.</div>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-4">
                        <div class="row align-items-center">
                            <label class="col-sm-4 col-form-label">Affiliating Institute at the time of publication<span class="ms-1" style="color: red;">*</span><span class="fa-solid fa-circle-info" data-bs-toggle="tooltip" data-bs-placement="top" title="${fieldInfo['Affiliating Institute at the time of publication']}"></span></label>
                            <div class = "col-sm-8">
                                <input type="text" class="form-control" placeholder="Enter Affiliating Institute at the time of publication" name = "aiop" required>
                                <div class="invalid-feedback">Please provide Affiliating Institute at the time of publication.-${i}</div>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-7">
                        <div class="row align-items-center">
                            <label class="col-sm-3 col-form-label">Indexed by<span class="ms-1" style="color: red;">*</span></label>
                            <div class="col-sm-9">
                                <div class="d-flex column-gap-4">
                                    <div class="form-check">
                                        <input type="radio" class="form-check-input" id="radio3-${i}" name="optradio1" value="S" required>
                                        <label class="form-check-label" for="radio3-${i}">SCI/SCIE/SSCI</label>
                                    </div>
                                    <div class="form-check">
                                        <input type="radio" class="form-check-input" id="radio4-${i}" name="optradio1" value="NS">
                                        <label class="form-check-label" for="radio4-${i}">Scopus</label>
                                    </div>
                                    <div class="form-check">
                                        <input type="radio" class="form-check-input" id="radio5-${i}" name="optradio1" value="ES">
                                        <label class="form-check-label" for="radio5-${i}">ESCI</label>
                                    </div>
                                    <div class="form-check">
                                        <input type="radio" class="form-check-input" id="radio6-${i}" name="optradio1" value="UGC">
                                        <label class="form-check-label" for="radio6-${i}">UGC</label>
                                    </div>
                                    <div class="form-check">
                                        <input type="radio" class="form-check-input" id="radio7-${i}" name="optradio1" value="O">
                                        <label class="form-check-label" for="radio7-${i}">Other</label>
                                    </div>
                                </div>
                                <div class="invalid-feedback">Please select an option.</div>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-5">
                        <div class="row align-items-center">
                            <label class="col-sm-4 col-form-label">Quartile<span class="ms-1" style="color: red;">*</span></label>
                            <div class="col-sm-8">
                                <div class="d-flex column-gap-4">
                                    <div class="form-check">
                                        <input type="radio" class="form-check-input" id="radio3-${i}" name="optradio" value="Q1" required>
                                        <label class="form-check-label" for="radio3">Q1</label>
                                    </div>
                                    <div class="form-check">
                                        <input type="radio" class="form-check-input" id="radio4-${i}" name="optradio" value="Q2">
                                        <label class="form-check-label" for="radio4-${i}">Q2</label>
                                    </div>
                                    <div class="form-check">
                                        <input type="radio" class="form-check-input" id="radio5-${i}" name="optradio" value="Q3">
                                        <label class="form-check-label" for="radio5-${i}">Q3</label>
                                    </div>
                                    <div class="form-check">
                                        <input type="radio" class="form-check-input" id="radio6-${i}" name="optradio" value="Q4">
                                        <label class="form-check-label" for="radio6-${i}">Q4</label>
                                    </div>
                                    <div class="form-check">
                                        <input type="radio" class="form-check-input" id="radio7-${i}" name="optradio" value="NA">
                                        <label class="form-check-label" for="radio7-${i}">NA</label>
                                    </div>
                                </div>
                                <div class="invalid-feedback">Please select an option.</div>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-4">
                        <div class="row align-items-center">
                            <label class="col-sm-4 col-form-label">Is SKIT student associated?<span class="ms-1" style="color: red;">*</span><span class="fa-solid fa-circle-info" data-bs-toggle="tooltip" data-bs-placement="top" title="${fieldInfo['Is SKIT student associated?']}"></span></label>
                            <div class="col-sm-8">
                                <div class="d-flex column-gap-4">
                                    <div class="form-check">
                                        <input type="radio" class="form-check-input" id="radio5-${i}" name="optradio2" value="y" required>
                                        <label class="form-check-label" for="radio5-${i}">Yes</label>
                                    </div>
                                    <div class="form-check">
                                        <input type="radio" class="form-check-input" id="radio6-${i}" name="optradio2" value="N">
                                        <label class="form-check-label" for="radio6-${i}">No</label>
                                    </div>
                                </div>
                                <div class="invalid-feedback">Please select an option.</div>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-4">
                        <div class="row align-items-center">
                            <label class="col-sm-4 col-form-label">If Yes , Write student(s) details (Program, Branch, RollNo/EnrollNo, Name)<span class="ms-1" style="color: red;">*</span><span class="fa-solid fa-circle-info" data-bs-toggle="tooltip" data-bs-placement="top" title="${fieldInfo['If Yes , Write student(s) details (Program, Branch, RollNo/EnrollNo, Name)']}"></span></label>
                            <div class = "col-sm-8">
                                <input type="text" class="form-control" placeholder="Enter Student details" name = "details" required>
                                <div class="invalid-feedback">Please provide student(s) details.</div>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-6">
                        <div class="row align-items-center">
                            <label class="col-sm-4 col-form-label">Upload Full Paper<span class="ms-1" style="color: red;">*</span><span class="fa-solid fa-circle-info" data-bs-toggle="tooltip" data-bs-placement="top" title="${fieldInfo['Upload Full Paper']}"></span>
                            <h5 class="font-small mt-2" style="font-size: 14px; color: gray;">Upload .pdf,.jpg,.jpeg,.png File Format(MAX SIZE:- 2MB)</h5></label>
                            <div class="col-sm-6">
                                <input type="file" class="form-control" accept=".pdf, image/jpeg, image/png" name="proof_file" required>
                                <div class="invalid-feedback">Please upload a PDF, JPG/JPEG or PNG file only.</div>
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
    } else if(form_number === '7') {
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
                                <div class="invalid-feedback">Please provide name of author(s).</div>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-4">
                        <div class="row align-items-center">
                            <label class="col-sm-4 col-form-label">Title of Conference<span class="ms-1" style="color: red;">*</span><span class="fa-solid fa-circle-info" data-bs-toggle="tooltip" data-bs-placement="top" title="${fieldInfo['Title of the Conference']}"></span></label>
                            <div class = "col-sm-8">
                                <input type="text" class="form-control" placeholder="Enter Title of the conference" name = "toc" required>
                                <div class="invalid-feedback">Please provide Title of Conference.</div>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-4">
                        <div class="row align-items-center">
                            <label class="col-sm-4 col-form-label">Title of Paper<span class="ms-1" style="color: red;">*</span></label>
                            <div class = "col-sm-8">
                                <input type="text" class="form-control" placeholder="Enter title of Paper" name = "top" required>
                                <div class="invalid-feedback">Please provide Title of Paper.</div>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-4">
                        <div class="row align-items-center">
                            <label class="col-sm-4 col-form-label">Title of the proceedings of the conference<span class="ms-1" style="color: red;">*</span><span class="fa-solid fa-circle-info" data-bs-toggle="tooltip" data-bs-placement="top" title="${fieldInfo['Title of the proceedings of the conference']}"></span></label>
                            <div class = "col-sm-8">
                                <input type="text" class="form-control" placeholder="Enter Title of the proceedings of the conference" name = "topc" required>
                                <div class="invalid-feedback">Please provide Title of the proceedings of the conference.</div>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-4">
                        <div class="row align-items-center">
                            <label class="col-sm-4 col-form-label">Level (National/ International)<span class="ms-1" style="color: red;">*</span></label>
                            <div class="col-sm-8">
                                <div class="d-flex column-gap-4">
                                    <div class="form-check">
                                        <input type="radio" class="form-check-input" id="radio1-${i}" name="optradio3" value="Na" required>
                                        <label class="form-check-label" for="radio1-${i}">National</label>
                                    </div>
                                    <div class="form-check">
                                        <input type="radio" class="form-check-input" id="radio2-${i}" name="optradio3" value="In">
                                        <label class="form-check-label" for="radio2-${i}">International</label>
                                    </div>
                                </div>
                                <div class="invalid-feedback">Please select level.</div>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-4">
                        <div class="row align-items-center">
                            <label class="col-sm-4 col-form-label">ISBN/ISSN number of the proceeding<span class="ms-1" style="color: red;">*</span></label>
                            <div class = "col-sm-8">
                                <input type="text" class="form-control" placeholder="Enter ISBN/ISSN number of the proceeding" name = "isnp" required>
                                <div class="invalid-feedback">Please provide ISBN/ISSN number of the proceeding.</div>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-4">
                        <div class="row align-items-center">
                            <label class="col-sm-4 col-form-label">Name of the Publisher<span class="ms-1" style="color: red;">*</span></label>
                            <div class = "col-sm-8">
                                <input type="text" class="form-control" placeholder="Enter name of publisher" name = "nop" required>
                                <div class="invalid-feedback">Please provide name of publisher.</div>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-4">
                        <div class="row align-items-center">
                            <label class="col-sm-4 col-form-label">Published Date<span class="ms-1" style="color: red;">*</span></label>
                            <div class="col-sm-8">
                                <input type="date" class="form-control" name = "begi_date" required>
                                <div class="invalid-feedback">Please provide published date.</div>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-4">
                        <div class="row align-items-center">
                            <label class="col-sm-4 col-form-label">Session<span class="ms-1" style="color: red;">*</span><span class="fa-solid fa-circle-info" data-bs-toggle="tooltip" data-bs-placement="top" title="${fieldInfo['Session']}"></span></label>
                            <div class="col-sm-8">
                                <select class="form-select custom-back-select" name="sessionyear" id="sessionyear" required>
                                    <option value="" selected disabled>Select your Session</option>
                                    <option value="2024-25">2024-25</option>
                                    <option value="2025-26">2025-26</option>
                                    <option value="2026-27">2026-27</option>
                                    <option value="2027-28">2027-28</option>
                                    <option value="2028-29">2028-29</option>
                                    <option value="2029-30">2029-30</option>
                                </select>
                                <div class="invalid-feedback">Please provide academic session.</div>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-4">
                        <div class="row align-items-center">
                            <label class="col-sm-4 col-form-label">DOI(Digital Object Identifier)<span class="ms-1" style="color: red;">*</span><span class="fa-solid fa-circle-info" data-bs-toggle="tooltip" data-bs-placement="top" title="${fieldInfo['DOI']}"></span></label>
                            <div class = "col-sm-8">
                                <input type="text" class="form-control" placeholder="Enter DOI(Digital Object Identifier)" name = "doi" required>
                                <div class="invalid-feedback">Please provide DOI(Digital Object Identifier).</div>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-4">
                        <div class="row align-items-center">
                            <label class="col-sm-4 col-form-label">Web Link<span class="ms-1" style="color: red;">*</span><span class="fa-solid fa-circle-info" data-bs-toggle="tooltip" data-bs-placement="top" title="${fieldInfo['Link to website of the Journal']}"></span></label>
                            <div class = "col-sm-8">
                                <input type="text" class="form-control" placeholder="Enter Link to website of the Journal" name = "lwj" required>
                                <div class="invalid-feedback">Please provide Link to website of the Journal starting with www., http://, or https://. or write na</div>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-4">
                        <div class="row align-items-center">
                            <label class="col-sm-4 col-form-label">Affiliating Institute at the time of publication<span class="ms-1" style="color: red;">*</span><span class="fa-solid fa-circle-info" data-bs-toggle="tooltip" data-bs-placement="top" title="${fieldInfo['Affiliating Institute at the time of publication']}"></span></label>
                            <div class = "col-sm-8">
                                <input type="text" class="form-control" placeholder="Enter Affiliating Institute at the time of publication" name = "aitp" required>
                                <div class="invalid-feedback">Please provide Affiliating Institute at the time of publication.</div>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-7">
                        <div class="row align-items-center">
                            <label class="col-sm-4 col-form-label">Indexed by<span class="ms-1" style="color: red;">*</span></label>
                            <div class="col-sm-8">
                                <input type="text" class="form-control" placeholder="Enter indexed by" name = "index_by" required>
                                <div class="invalid-feedback">Please provide Indexed by.</div>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-4">
                        <div class="row align-items-center">
                            <label class="col-sm-4 col-form-label">Is SKIT student associated?<span class="ms-1" style="color: red;">*</span><span class="fa-solid fa-circle-info" data-bs-toggle="tooltip" data-bs-placement="top" title="${fieldInfo['Is SKIT student associated?']}"></span></label>
                            <div class="col-sm-8">
                                <div class="d-flex column-gap-4">
                                    <div class="form-check">
                                        <input type="radio" class="form-check-input" id="radio5-${i}" name="optradio2" value="y" required>
                                        <label class="form-check-label" for="radio5-${i}">Yes</label>
                                    </div>
                                    <div class="form-check">
                                        <input type="radio" class="form-check-input" id="radio6-${i}" name="optradio2" value="N">
                                        <label class="form-check-label" for="radio6-${i}">No</label>
                                    </div>
                                </div>
                                <div class="invalid-feedback">Please select an option.</div>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-4">
                        <div class="row align-items-center">
                            <label class="col-sm-4 col-form-label">If Yes , Write student(s) details (Program, Branch, RollNo/EnrollNo, Name)<span class="ms-1" style="color: red;">*</span><span class="fa-solid fa-circle-info" data-bs-toggle="tooltip" data-bs-placement="top" title="${fieldInfo['If Yes , Write student(s) details (Program, Branch, RollNo/EnrollNo, Name)']}"></span></label>
                            <div class = "col-sm-8">
                                <input type="text" class="form-control" placeholder="Enter Student details" name = "details" required>
                                <div class="invalid-feedback">Please provide student(s) details.</div>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-6">
                        <div class="row align-items-center">
                            <label class="col-sm-4 col-form-label">Upload Full Paper<span class="ms-1" style="color: red;">*</span><span class="fa-solid fa-circle-info" data-bs-toggle="tooltip" data-bs-placement="top" title="${fieldInfo['Upload Full Paper']}"></span>
                            <h5 class="font-small mt-2" style="font-size: 14px; color: gray;">Upload .pdf,.jpg,.jpeg,.png File Format(MAX SIZE:- 2MB)</h5></label>
                            <div class="col-sm-6">
                                <input type="file" class="form-control" accept=".pdf, image/jpeg, image/png" name="proof_file" required>
                                <div class="invalid-feedback">Please upload a PDF, JPG/JPEG or PNG file only.</div>
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
    } else if(form_number === '8') {
        subForm.innerHTML = `
            <div class="sub-form-title" style = "font-size: 1.5rem; color: #667eea;"><b>${category} #${i}</b></div>
            <input type = "hidden" name = "csrfmiddlewaretoken" value = "${csrfToken}">
            <div class="sub-form-fields">
                <div class="row g-3">
                    <div class="col-md-4">
                        <div class="row align-items-center">
                            <label for="top" class="col-sm-4 col-form-label">Name of the author/editor<span class="ms-1" style="color: red;">*</span></label>
                            <div class = "col-md-8">
                                <input type="text" class="form-control" id="toc" placeholder="Enter name of author" name="noa" required>
                                <div class="invalid-feedback">Please provide name of author(s).</div>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-4">
                        <div class="row align-items-center">
                            <label class="col-sm-4 col-form-label">Title of the book<span class="ms-1" style="color: red;">*</span></label>
                            <div class = "col-sm-8">
                                <input type="text" class="form-control" placeholder="Enter Title of the conference" name = "tob" required>
                                <div class="invalid-feedback">Please provide Title of the book.</div>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-4">
                        <div class="row align-items-center">
                            <label class="col-sm-4 col-form-label">Title of the chapter Published<span class="ms-1" style="color: red;">*</span><span class="fa-solid fa-circle-info" data-bs-toggle="tooltip" data-bs-placement="top" title="${fieldInfo['Title of the chapter Published']}"></span></label>
                            <div class = "col-sm-8">
                                <input type="text" class="form-control" placeholder="Enter title of Paper" name = "top" required>
                                <div class="invalid-feedback">Please provide Title of the chapter Published.</div>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-4">
                        <div class="row align-items-center">
                            <label class="col-sm-4 col-form-label">Level (National/ International)<span class="ms-1" style="color: red;">*</span></label>
                            <div class="col-sm-8">
                                <div class="d-flex column-gap-4">
                                    <div class="form-check">
                                        <input type="radio" class="form-check-input" id="radio1-${i}" name="optradio3" value="Na" required>
                                        <label class="form-check-label" for="radio1-${i}">National</label>
                                    </div>
                                    <div class="form-check">
                                        <input type="radio" class="form-check-input" id="radio2-${i}" name="optradio3" value="In">
                                        <label class="form-check-label" for="radio2-${i}">International</label>
                                    </div>
                                </div>
                                <div class="invalid-feedback">Please select level.</div>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-4">
                        <div class="row align-items-center">
                            <label class="col-sm-4 col-form-label">ISBN<span class="ms-1" style="color: red;">*</span></label>
                            <div class = "col-sm-8">
                                <input type="text" class="form-control" placeholder="Enter ISBN" name = "isbn" required>
                                <div class="invalid-feedback">Please enter ISBN.</div>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-4">
                        <div class="row align-items-center">
                            <label class="col-sm-4 col-form-label">Name of the Publisher<span class="ms-1" style="color: red;">*</span></label>
                            <div class = "col-sm-8">
                                <input type="text" class="form-control" placeholder="Enter name of publisher" name = "nop" required>
                                <div class="invalid-feedback">Please provide name of publisher.</div>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-4">
                        <div class="row align-items-center">
                            <label class="col-sm-4 col-form-label">Published Date<span class="ms-1" style="color: red;">*</span></label>
                            <div class="col-sm-8">
                                <input type="date" class="form-control" name = "begi_date" required>
                                <div class="invalid-feedback">Please provide published date.</div>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-4">
                        <div class="row align-items-center">
                            <label class="col-sm-4 col-form-label">Session<span class="ms-1" style="color: red;">*</span><span class="fa-solid fa-circle-info" data-bs-toggle="tooltip" data-bs-placement="top" title="${fieldInfo['Session']}"></span></label>
                            <div class="col-sm-8">
                                <select class="form-select custom-back-select" name="sessionyear" id="sessionyear" required>
                                    <option value="" selected disabled>Select your Session</option>
                                    <option value="2024-25">2024-25</option>
                                    <option value="2025-26">2025-26</option>
                                    <option value="2026-27">2026-27</option>
                                    <option value="2027-28">2027-28</option>
                                    <option value="2028-29">2028-29</option>
                                    <option value="2029-30">2029-30</option>
                                </select>
                                <div class="invalid-feedback">Please select academic session.</div>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-4">
                        <div class="row align-items-center">
                            <label class="col-sm-4 col-form-label">DOI(Digital Object Identifier)<span class="ms-1" style="color: red;">*</span><span class="fa-solid fa-circle-info" data-bs-toggle="tooltip" data-bs-placement="top" title="${fieldInfo['DOI']}"></span></label>
                            <div class = "col-sm-8">
                                <input type="text" class="form-control" placeholder="Enter DOI(Digital Object Identifier)" name = "doi" required>
                                <div class="invalid-feedback">Please provide DOI(Digital Object Identifier).</div>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-4">
                        <div class="row align-items-center">
                            <label class="col-sm-4 col-form-label">Web Link<span class="ms-1" style="color: red;">*</span><span class="fa-solid fa-circle-info" data-bs-toggle="tooltip" data-bs-placement="top" title="${fieldInfo['Link to website of the Journal']}"></span></label>
                            <div class = "col-sm-8">
                                <input type="text" class="form-control" placeholder="Enter Link to website of the Journal" name = "lwj" required>
                                <div class="invalid-feedback">Please provide Link to website of the Journal starting with www., http://, or https://. or write na</div>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-8">
                        <div class="row align-items-center">
                            <label class="col-sm-4 col-form-label">Affiliating Institute at the time of publication<span class="ms-1" style="color: red;">*</span><span class="fa-solid fa-circle-info" data-bs-toggle="tooltip" data-bs-placement="top" title="${fieldInfo['Affiliating Institute at the time of publication']}"></span></label>
                            <div class = "col-sm-8">
                                <input type="text" class="form-control" placeholder="Enter Affiliating Institute at the time of publication" name = "aitp" required>
                                <div class="invalid-feedback">Please provide Affiliating Institute at the time of publication.</div>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-7">
                        <div class="row align-items-center">
                            <label class="col-sm-4 col-form-label">Indexed by<span class="ms-1" style="color: red;">*</span></label>
                            <div class="col-sm-8">
                                <input type="text" class="form-control" placeholder="Enter indexed by" name = "index_by" required>
                                <div class="invalid-feedback">Please provide Indexed by.</div>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-4">
                        <div class="row align-items-center">
                            <label class="col-sm-4 col-form-label">Is SKIT student associated?<span class="ms-1" style="color: red;">*</span><span class="fa-solid fa-circle-info" data-bs-toggle="tooltip" data-bs-placement="top" title="${fieldInfo['Is SKIT student associated?']}"></span></label>
                            <div class="col-sm-8">
                                <div class="d-flex column-gap-4">
                                    <div class="form-check">
                                        <input type="radio" class="form-check-input" id="radio5-${i}" name="optradio2" value="y" required>
                                        <label class="form-check-label" for="radio5-${i}">Yes</label>
                                    </div>
                                    <div class="form-check">
                                        <input type="radio" class="form-check-input" id="radio6-${i}" name="optradio2" value="N">
                                        <label class="form-check-label" for="radio6-${i}">No</label>
                                    </div>
                                </div>
                                <div class="invalid-feedback">Please select an option.</div>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-8">
                        <div class="row align-items-center">
                            <label class="col-sm-4 col-form-label">If Yes , Write student(s) details (Program, Branch, RollNo/EnrollNo, Name)<span class="ms-1" style="color: red;">*</span><span class="fa-solid fa-circle-info" data-bs-toggle="tooltip" data-bs-placement="top" title="${fieldInfo['If Yes , Write student(s) details (Program, Branch, RollNo/EnrollNo, Name)']}"></span></label>
                            <div class = "col-sm-8">
                                <input type="text" class="form-control" placeholder="Enter Student details" name = "details" required>
                                <div class="invalid-feedback">Please provide student(s) details.</div>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-6">
                        <div class="row align-items-center">
                            <label class="col-sm-4 col-form-label">Upload Proof (Book Chapter/Front Page/Document etc.)<span class="ms-1" style="color: red;">*</span><span class="fa-solid fa-circle-info" data-bs-toggle="tooltip" data-bs-placement="top" title="${fieldInfo['Upload Full Paper']}"></span>
                            <h5 class="font-small mt-2" style="font-size: 14px; color: gray;">Upload .pdf,.jpg,.jpeg,.png File Format(MAX SIZE:- 2MB)</h5></label>
                            <div class="col-sm-6">
                                <input type="file" class="form-control" accept=".pdf, image/jpeg, image/png" name="proof_file" required>
                                <div class="invalid-feedback">Please upload a PDF, JPG/JPEG or PNG file only.</div>
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
    } else if (form_number === '9') {
        subForm.innerHTML = `
            <div class="sub-form-title" style = "font-size: 1.5rem; color: #667eea;"><b>${category} #${i}</b></div>
            <input type = "hidden" name = "csrfmiddlewaretoken" value = "${csrfToken}">
            <div class="sub-form-fields">
                <div class="row g-3">
                    <div class="col-md-4">
                        <div class="row align-items-center">
                            <label class="col-sm-4 col-form-label">Session<span class="ms-1" style="color: red;">*</span><span class="fa-solid fa-circle-info" data-bs-toggle="tooltip" data-bs-placement="top" title="${fieldInfo['Session']}"></span></label>
                            <div class="col-sm-8">
                                <select class="form-select custom-back-select" name="sessionyear" id="sessionyear" required>
                                    <option value="" selected disabled>Select your Session</option>
                                    <option value="2024-25">2024-25</option>
                                    <option value="2025-26">2025-26</option>
                                    <option value="2026-27">2026-27</option>
                                    <option value="2027-28">2027-28</option>
                                    <option value="2028-29">2028-29</option>
                                    <option value="2029-30">2029-30</option>
                                </select>
                                <div class="invalid-feedback">Please select Academic Session.-${i}</div>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-4">
                        <div class="row align-items-center">
                            <label class="col-sm-4 col-form-label">Status of Patent<span class="ms-1" style="color: red;">*</span><span class="fa-solid fa-circle-info" data-bs-toggle="tooltip" data-bs-placement="top" title="${fieldInfo['Is the Patent granted ?']}"></span></label>
                            <div class="col-sm-8">
                                <div class="d-flex column-gap-4">
                                    <div class="form-check">
                                        <input type="radio" class="form-check-input" id="radio5-${i}" name="optradio1" value="P" required>
                                        <label class="form-check-label" for="radio5-${i}">Published</label>
                                    </div>
                                    <div class="form-check">
                                        <input type="radio" class="form-check-input" id="radio6-${i}" name="optradio1" value="G">
                                        <label class="form-check-label" for="radio6-${i}">Granted</label>
                                    </div>
                                </div>
                                <div class="invalid-feedback">Please select an option.</div>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-4">
                        <div class="row align-items-center">
                            <label class="col-sm-4 col-form-label">Application ID<span class="ms-1" style="color: red;">*</span></label>
                            <div class = "col-sm-8">
                                <input type="text" class="form-control" placeholder="Enter Application ID" name = "ag" required>
                                <div class="invalid-feedback">Please provide Application ID.</div>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-4">
                        <div class="row align-items-center">
                            <label for="top" class="col-sm-4 col-form-label">Granted ID<span class="ms-1" style="color: red;">*</span></label>
                            <div class = "col-md-8">
                                <input type="text" class="form-control" id="toc" placeholder="Enter Granted ID" name="nof" required>
                                <div class="invalid-feedback">Please provide Granted ID.</div>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-4">
                        <div class="row align-items-center">
                            <label class="col-sm-4 col-form-label">Type of Patent<span class="ms-1" style="color: red;">*</span><span class="fa-solid fa-circle-info" data-bs-toggle="tooltip" data-bs-placement="top" title="${fieldInfo['Is the Patent granted ?']}"></span></label>
                            <div class="col-sm-8">
                                <div class="d-flex column-gap-4">
                                    <div class="form-check">
                                        <input type="radio" class="form-check-input" id="radio5-${i}" name="optradio2" value="I" required>
                                        <label class="form-check-label" for="radio5">Innovation</label>
                                    </div>
                                    <div class="form-check">
                                        <input type="radio" class="form-check-input" id="radio6-${i}" name="optradio2" value="D">
                                        <label class="form-check-label" for="radio6-${i}">Design</label>
                                    </div>
                                </div>
                                <div class="invalid-feedback">Please select an option.</div>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-4">
                        <div class="row align-items-center">
                            <label class="col-sm-4 col-form-label">Title of Patent<span class="ms-1" style="color: red;">*</span></label>
                            <div class = "col-sm-8">
                                <input type="text" class="form-control" placeholder="Enter title of Patent" name = "top" required>
                                <div class="invalid-feedback">Please provide Title of Patent.</div>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-4">
                        <div class="row align-items-center">
                            <label class="col-sm-4 col-form-label">Granted Country<span class="ms-1" style="color: red;">*</span></label>
                            <div class = "col-sm-8">
                                <input type="text" class="form-control" placeholder="Enter detail" name = "gc" required>
                                <div class="invalid-feedback">Please provide Granted Country.</div>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-4">
                        <div class="row align-items-center">
                            <label class="col-sm-4 col-form-label">Patent Filed Date<span class="ms-1" style="color: red;">*</span></label>
                            <div class="col-sm-8">
                                <input type="date" class="form-control" name = "filed_date" required>
                                <div class="invalid-feedback">Please provide Patent Filed Date.</div>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-4">
                        <div class="row align-items-center">
                            <label class="col-sm-4 col-form-label">Publication Date<span class="ms-1" style="color: red;">*</span></label>
                            <div class="col-sm-8">
                                <input type="date" class="form-control" name = "begi_date" required>
                                <div class="invalid-feedback">Please provide Publication Date.</div>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-4">
                        <div class="row align-items-center">
                            <label class="col-sm-4 col-form-label">Is SKIT student associated?<span class="ms-1" style="color: red;">*</span><span class="fa-solid fa-circle-info" data-bs-toggle="tooltip" data-bs-placement="top" title="${fieldInfo['Is SKIT student associated?(Patent)']}"></span></label>
                            <div class="col-sm-8">
                                <div class="d-flex column-gap-4">
                                    <div class="form-check">
                                        <input type="radio" class="form-check-input" id="radio5-${i}" name="optradio" value="y" required>
                                        <label class="form-check-label" for="radio5-${i}">Yes</label>
                                    </div>
                                    <div class="form-check">
                                        <input type="radio" class="form-check-input" id="radio6-${i}" name="optradio" value="N">
                                        <label class="form-check-label" for="radio6-${i}">No</label>
                                    </div>
                                </div>
                                <div class="invalid-feedback">Please select an option.</div>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-4">
                        <div class="row align-items-center">
                            <label class="col-sm-4 col-form-label">If Yes , Write student(s) details (Program, Branch, RollNo/EnrollNo, Name)<span class="ms-1" style="color: red;">*</span><span class="fa-solid fa-circle-info" data-bs-toggle="tooltip" data-bs-placement="top" title="${fieldInfo['If Yes , Write student(s) details (Program, Branch, RollNo/EnrollNo, Name)']}"></span></label>
                            <div class = "col-sm-8">
                                <input type="text" class="form-control" placeholder="Enter Student details" name = "details" required>
                                <div class="invalid-feedback">Please provide student(s) details.</div>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-4">
                        <div class="row align-items-center">
                            <label class="col-sm-4 col-form-label">Link<span class="ms-1" style="color: red;">*</span><span class="fa-solid fa-circle-info" data-bs-toggle="tooltip" data-bs-placement="top" title="${fieldInfo['Link to website of the Journal']}"></span></label>
                            <div class = "col-sm-8">
                                <input type="text" class="form-control" placeholder="Enter Link to website of the Journal" name = "link" required>
                                <div class="invalid-feedback">Please provide a valid link starting with www., http://, or https:// or write na</div>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-6">
                        <div class="row align-items-center">
                            <label class="col-sm-4 col-form-label">Upload Proof<span class="ms-1" style="color: red;">*</span><span class="fa-solid fa-circle-info" data-bs-toggle="tooltip" data-bs-placement="top" title="${fieldInfo['Upload Proof (Patent)']}"></span>
                            <h5 class="font-small mt-2" style="font-size: 14px; color: gray;">Upload .pdf,.jpg,.jpeg,.png File Format(MAX SIZE:- 2MB)</h5></label>
                            <div class="col-sm-6">
                                <input type="file" class="form-control" accept=".pdf,.jpg,.jpeg,.png" name="proof_file" required>
                                <div class="invalid-feedback">Please upload a PDF, JPG/JPEG or PNG file only.</div>
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
    } else if (form_number === '10') {
        subForm.innerHTML = `
            <div class="sub-form-title" style = "font-size: 1.5rem; color: #667eea;"><b>${category} #${i}</b></div>
            <input type = "hidden" name = "category" value = "${categoryValue[category]}">
            <input type = "hidden" name = "csrfmiddlewaretoken" value = "${csrfToken}">
            <div class="sub-form-fields">
                <div class="row g-3">
                    <div class="col-md-4">
                        <div class="row align-items-center">
                            <label class="col-sm-4 col-form-label">Session<span class="ms-1" style="color: red;">*</span><span class="fa-solid fa-circle-info" data-bs-toggle="tooltip" data-bs-placement="top" title="${fieldInfo['Session']}"></span></label>
                            <div class="col-sm-8">
                                <select class="form-select custom-back-select" name="sessionyear" id="sessionyear" required>
                                    <option value="" selected disabled>Select your Session</option>
                                    <option value="2024-25">2024-25</option>
                                    <option value="2025-26">2025-26</option>
                                    <option value="2026-27">2026-27</option>
                                    <option value="2027-28">2027-28</option>
                                    <option value="2028-29">2028-29</option>
                                    <option value="2029-30">2029-30</option>
                                </select>
                                <div class="invalid-feedback">Please select Session.</div>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-4">
                        <div class="row align-items-center">
                            <label for="top" class="col-sm-4 col-form-label">Name of the student Guided<span class="ms-1" style="color: red;">*</span></label>
                            <div class = "col-md-8">
                                <input type="text" class="form-control custom-back" id="top" placeholder="Enter Name of the student Guided" name="nos" required>
                                <div class="invalid-feedback">Please provide Name of the student Guided.</div>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-4">
                        <div class="row align-items-center">
                            <label class="col-sm-4 col-form-label">Enrollment Number of Student<span class="ms-1" style="color: red;">*</span></label>
                            <div class="col-sm-8">
                                <input type="text" class="form-control" placeholder="Enter Enrollment Number of Student" name = "ens" required>
                                <div class="invalid-feedback">Please enter Enrollment Number of Student.</div>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-4">
                        <div class="row align-items-center">
                            <label class="col-sm-4 col-form-label">University Roll Number of Student<span class="ms-1" style="color: red;">*</span></label>
                            <div class="col-sm-8">
                                <input type="text" class="form-control" placeholder="Enter organizer" name = "urns" required>
                                <div class="invalid-feedback">Please enter University Roll Number of Student.</div>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-4">
                        <div class="row align-items-center">
                            <label class="col-sm-4 col-form-label">Enrollment Year of Student<span class="ms-1" style="color: red;">*</span></label>
                            <div class="col-sm-8">
                                <select class="form-select custom-back-select" name="enrollmentyear" id="enrollmentyear" required>
                                    <option value="" selected disabled>Select enrollment year</option>
                                    <option value="2023">2023</option>
                                    <option value="2024">2024</option>
                                    <option value="2025">2025</option>
                                </select>
                                <div class="invalid-feedback">Please select Enrollment Year of Student.</div>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-4">
                        <div class="row align-items-center">
                            <label class="col-sm-4 col-form-label">Title of the Dissertation<span class="ms-1" style="color: red;">*</span></label>
                            <div class="col-sm-8">
                                <input type="text" class="form-control" placeholder="Enter organizer" name = "tod" required>
                                <div class="invalid-feedback">Please enter Title of the Dissertation.</div>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-4">
                        <div class="row align-items-center">
                            <label class="col-sm-4 col-form-label">Supervisor / Co-supervisor<span class="ms-1" style="color: red;">*</span></label>
                            <div class="col-sm-8">
                                <div class="d-flex column-gap-4">
                                    <div class="form-check">
                                        <input type="radio" class="form-check-input" id="radio5-${i}" name="optradio2" value="S" required>
                                        <label class="form-check-label" for="radio5-${i}">Supervisor</label>
                                    </div>
                                    <div class="form-check">
                                        <input type="radio" class="form-check-input" id="radio6-${i}" name="optradio2" value="CS">
                                        <label class="form-check-label" for="radio6-${i}">Co-supervisor</label>
                                    </div>
                                </div>
                                <div class="invalid-feedback">Please select an option.</div>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-4">
                        <div class="row align-items-center">
                            <label class="col-sm-4 col-form-label">Date of Viva-Voce<span class="ms-1" style="color: red;">*</span></label>
                            <div class="col-sm-8">
                                <input type="date" class="form-control" name = "dov" required>
                                <div class="invalid-feedback">Please provide Date of Viva-Voce.</div>
                            </div>
                        </div>
                    </div>
                        <div class="col-md-4">
                        <div class="row align-items-center">
                            <label class="col-sm-4 col-form-label">Name of external examiner<span class="ms-1" style="color: red;">*</span></label>
                            <div class="col-sm-8">
                                <input type="text" class="form-control" placeholder="Enter Name of external examiner" name = "noe" required>
                                <div class="invalid-feedback">Please provide Name of external examiner.</div>
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
    } else if (form_number === '11') {
        subForm.innerHTML = `
            <div class="sub-form-title" style = "font-size: 1.5rem; color: #667eea;"><b>${category} #${i}</b></div>
            <input type = "hidden" name = "category" value = "${categoryValue[category]}">
            <input type = "hidden" name = "csrfmiddlewaretoken" value = "${csrfToken}">
            <div class="sub-form-fields">
                <div class="row g-3">
                    <div class="col-md-6 mt-4">
                        <div class="row align-items-center">
                            <label class="col-sm-4 col-form-label">Session<span class="ms-1" style="color: red;">*</span><span class="fa-solid fa-circle-info" data-bs-toggle="tooltip" data-bs-placement="top" title="${fieldInfo['Session']}"></span></label>
                            <div class="col-sm-8">
                                <select class="form-select custom-back-select" name="sessionyear" id="sessionyear" required>
                                    <option value="" selected disabled>Select your Session</option>
                                    <option value="2024-25">2024-25</option>
                                    <option value="2025-26">2025-26</option>
                                    <option value="2026-27">2026-27</option>
                                    <option value="2027-28">2027-28</option>
                                    <option value="2028-29">2028-29</option>
                                    <option value="2029-30">2029-30</option>
                                </select>
                                <div class="invalid-feedback">Please select Session.</div>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-6">
                        <div class="row align-items-center">
                            <label for="top" class="col-sm-4 col-form-label">Title of Event/ Exam Name<span class="ms-1" style="color: red;">*</span><span class="fa-solid fa-circle-info" data-bs-toggle="tooltip" data-bs-placement="top" title="${fieldInfo['Title of Event/ Exam Name']}"></span></label>
                            <div class = "col-md-8">
                                <input type="text" class="form-control custom-back" id="top" placeholder="Enter Name of the student Guided" name="toe" required>
                                <div class="invalid-feedback">Please provide Title of Event/ Exam Name.</div>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-6">
                        <div class="row align-items-center">
                            <label class="col-sm-4 col-form-label">Subject Area/Subject Name/Lab Name/Session Name<span class="ms-1" style="color: red;">*</span><span class="fa-solid fa-circle-info" data-bs-toggle="tooltip" data-bs-placement="top" title="${fieldInfo['Subject Area/Subject Name/Lab Name/Session Name']}"></span></label>
                            <div class="col-sm-8">
                                <input type="text" class="form-control" placeholder="Enter Enrollment Number of Student" name = "sa" required>
                                <div class="invalid-feedback">Please enter Subject Area/Subject Name/Lab Name/Session Name.</div>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-12">
                        <div class="row align-items-center">
                            <label class="col-sm-2 col-form-label">Resource Person Type<span class="ms-1" style="color: red;">*</span></label>
                            <div class="col-sm-10">
                                <div class="d-flex column-gap-4">
                                    <div class="form-check">
                                        <input type="radio" class="form-check-input" id="radio5-${i}" name="optradio2" value="EE(UG)" required>
                                        <label class="form-check-label" for="radio5-${i}">External Examination (UG)</label>
                                    </div>
                                    <div class="form-check">
                                        <input type="radio" class="form-check-input" id="radio6-${i}" name="optradio2" value="EE(PG)">
                                        <label class="form-check-label" for="radio6-${i}">External Examination (PG)</label>
                                    </div>
                                    <div class="form-check">
                                        <input type="radio" class="form-check-input" id="radio7-${i}" name="optradio2" value="EBM">
                                        <label class="form-check-label" for="radio7-${i}">Editorial Board Member</label>
                                    </div>
                                    <div class="form-check">
                                        <input type="radio" class="form-check-input" id="radio8-${i}" name="optradio2" value="JM">
                                        <label class="form-check-label" for="radio8-${i}">Jury Member</label>
                                    </div>
                                    <div class="form-check">
                                        <input type="radio" class="form-check-input" id="radio9-${i}" name="optradio2" value="R">
                                        <label class="form-check-label" for="radio9-${i}">Reviewer</label>
                                    </div>
                                    <div class="form-check">
                                        <input type="radio" class="form-check-input" id="radio10-${i}" name="optradio2" value="SC">
                                        <label class="form-check-label" for="radio10-${i}">Session Chair</label>
                                    </div>
                                    <div class="form-check">
                                        <input type="radio" class="form-check-input" id="radio11-${i}" name="optradio2" value="E">
                                        <label class="form-check-label" for="radio11-${i}">Expert</label>
                                    </div>
                                    <div class="form-check">
                                        <input type="radio" class="form-check-input" id="radio12-${i}" name="optradio2" value="S">
                                        <label class="form-check-label" for="radio12-${i}">Speaker</label>
                                    </div>
                                    <div class="form-check">
                                        <input type="radio" class="form-check-input" id="radio13-${i}" name="optradio2" value="KNS">
                                        <label class="form-check-label" for="radio13-${i}">Key Note Speaker</label>
                                    </div>
                                </div>
                                <div class="d-flex column-gap-4 mt-3">
                                    <div class="form-check">
                                        <input type="radio" class="form-check-input" id="radio6-${i}" name="optradio2" value="T">
                                        <label class="form-check-label" for="radio6-${i}">Trainer</label>
                                    </div>
                                    <div class="form-check">
                                        <input type="radio" class="form-check-input" id="radio7-${i}" name="optradio2" value="TCM">
                                        <label class="form-check-label" for="radio7-${i}">Technical Committee Member</label>
                                    </div>
                                    <div class="form-check">
                                        <input type="radio" class="form-check-input" id="radio8-${i}" name="optradio2" value="DET">
                                        <label class="form-check-label" for="radio8-${i}">Delivered Expert Lecture/Talk</label>
                                    </div>
                                    <div class="form-check">
                                        <input type="radio" class="form-check-input" id="radio9-${i}" name="optradio2" value="DIT">
                                        <label class="form-check-label" for="radio9-${i}">Delivered Invited Talk</label>
                                    </div>
                                    <div class="form-check">
                                        <input type="radio" class="form-check-input" id="radio10-${i}" name="optradio2" value="BM">
                                        <label class="form-check-label" for="radio10-${i}">BOS Member</label>
                                    </div>
                                    <div class="form-check">
                                        <input type="radio" class="form-check-input" id="radio11-${i}" name="optradio2" value="DM">
                                        <label class="form-check-label" for="radio11-${i}">DRC Member</label>
                                    </div>
                                    <div class="form-check">
                                        <input type="radio" class="form-check-input" id="radio12-${i}" name="optradio2" value="O">
                                        <label class="form-check-label" for="radio12-${i}">Other</label>
                                    </div>
                                </div>
                                <div class="invalid-feedback">Please select Resource Person Type.</div>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-6">
                        <div class="row align-items-center">
                            <label class="col-sm-4 col-form-label">Duration of event (in days)<span class="ms-1" style="color: red;">*</span></label>
                            <div class="col-sm-8">
                                <input type="number" class="form-control" placeholder="Enter no. of days" name = "doe" required>
                                <div class="invalid-feedback">Please enter Duration of event.</div>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-6 mt-4">
                        <div class="row align-items-center">
                            <label class="col-sm-4 col-form-label">From Date<span class="ms-1" style="color: red;">*</span></label>
                            <div class="col-sm-8">
                                <input type="date" class="form-control" name = "begi_date" required>
                                <div class="invalid-feedback">Please provide From Date.</div>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-6 mt-4">
                        <div class="row align-items-center">
                            <label class="col-sm-4 col-form-label">To Date<span class="ms-1" style="color: red;">*</span></label>
                            <div class="col-sm-8">
                                <input type="date" class="form-control" name = "end_date" required>
                                <div class="invalid-feedback">Please provide To Date.</div>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-6 mt-4">
                        <div class="row align-items-center">
                            <label class="col-sm-4 col-form-label">Venue<span class="ms-1" style="color: red;">*</span></label>
                            <div class="col-sm-8">
                                <input type="text" class="form-control" placeholder="Enter venue of event" name = "venue" required>
                                <div class="invalid-feedback">Please provide Venue.</div>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-6 mt-4">
                        <div class="row align-items-center">
                            <label class="col-sm-5 col-form-label">Proof(Certificate/Mail)<span class="ms-1" style="color: red;">*</span><span class="fa-solid fa-circle-info" data-bs-toggle="tooltip" data-bs-placement="top" title="${fieldInfo['Proof (Certificate/Mail)']}"></span>
                            <h5 class="font-small mt-2" style="font-size: 14px; color: gray;">Upload .pdf,.jpg,.jpeg,.png File Format(MAX SIZE:- 2MB)</h5></label>
                            <div class="col-sm-7">
                                <input type="file" class="form-control" accept=".pdf,.jpg,.jpeg,.png" name="proof_file" required>
                                <div class="invalid-feedback">Please upload a PDF, JPG/JPEG or PNG file only.</div>
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

    // DISCARD (X) button
    const discardBtn = subForm.querySelector(".discard-btn");
    discardBtn.addEventListener("click", () => handleDiscard(subForm));

    // ADD FORM button
    const addBtn = subForm.querySelector(".btn-addform");
    addBtn.addEventListener("click", () => {
      buildForm(currentCategory); // recursive call for the same category form generation
      updateFormCountUI();
      refreshAddFormButtonVisibility();
      const newForms = subFormsContainer.querySelectorAll(".sub-form");
      newForms[newForms.length - 1].scrollIntoView({ behavior: "smooth", block: "center" });
    });
}

// keeps the visible titles sequential (FDP #1, FDP #2, ...) after a discard
  function renumberForms() {
    getLiveForms().forEach((subForm, idx) => {
      const category = subForm.dataset.category; 
      subForm.querySelector(".sub-form-heading").textContent = `${category} #${idx + 1}`;
    });
  }

function handleDiscard(subForm) {
    const confirmed = confirm("Discard this form? Any data entered in it will be lost.");
    if (!confirmed) return;

    subForm.remove();
    renumberForms();
    updateFormCountUI();
    refreshAddFormButtonVisibility();
}

// Only the LAST generated form should show the "+ Add Form" button.
function refreshAddFormButtonVisibility() {
    const allForms = getLiveForms();
    allForms.forEach((formEl, idx) => {
        const addBtn = formEl.querySelector(".btn-addform");
        if (!addBtn) return; // early stopping of the form add btn 
        addBtn.style.display = idx === allForms.length - 1 ? "inline-block" : "none";
    });
}

// shows a standalone "+ Add Form" button when every generated form has
// been discarded but a category is still selected, so the user isn't stuck.
function toggleRegenerateButton(liveCount) {
    const shouldShow = liveCount === 0 && !!currentCategory;
    regenerateBtn.style.display = shouldShow ? "inline-block" : "none";
}

function getLiveForms() {
    return subFormsContainer.querySelectorAll(".sub-form");
}

function updateFormCountUI() {
    const liveCount = getLiveForms().length;
    // console.log(liveCount);
    subformCount.textContent = `${liveCount} form${liveCount === 1 ? "" : "s"}`;
    emptyStateText.style.display = liveCount === 0 ? "block" : "none";
    toggleRegenerateButton(liveCount);
}

/* ---------- regenerate button (shown after all forms discarded) ---------- */

  regenerateBtn.addEventListener("click", () => {
    if (!currentCategory) return;
    buildForm(currentCategory);
    updateFormCountUI();
    refreshAddFormButtonVisibility();
  });

  /* ---------- back-to-top button ---------- */

  const SHOW_AFTER_PX = 320;

  function toggleBackToTopVisibility() {
    if (window.scrollY > SHOW_AFTER_PX) {
      backToTopBtn.classList.add("show");
    } else {
      backToTopBtn.classList.remove("show");
    }
  }

  window.addEventListener("scroll", toggleBackToTopVisibility, { passive: true });

  backToTopBtn.addEventListener("click", () => {
    window.scrollTo({ top: 0, behavior: "smooth" });
  });

  /* ---------- init ---------- */
  toggleBackToTopVisibility();
  updateFormCountUI();

function attachLinkValidation() {
    const linkFields = document.querySelectorAll('input[name="link"], input[name="lwj"], input[name="lrsj"], input[name="lap"]');
    // Updated pattern: REQUIRES either http://, https://, or www. at the start
    const urlPattern = /^(https?:\/\/|www\.)\S{2,}$|^(na|NA)$/i;

    linkFields.forEach(field => {
       field.removeAttribute('pattern'); // Remove pattern attribute to prevent HTML5 validation conflicts

        field.addEventListener('blur', function() {
            validateLinkField(this, urlPattern);
        });
        field.addEventListener('input', function() {
            validateLinkField(this, urlPattern);
        });
    });
}
function stopScrollNumberIncrement() {
    const numberInputs = document.querySelectorAll('input[type="number"]')

    numberInputs.forEach(function(input) {
        input.addEventListener('wheel', function(event) {
            event.preventDefault();
        }, {passive : false});
    });
}

function validateLinkField(field, pattern) {
    const val = field.value.trim();

    if (!pattern.test(field.value)) {
        field.classList.add("is-invalid");
        field.classList.remove("is-valid");
    } else {
        field.classList.add("is-valid");
        field.classList.remove("is-invalid");
    }
}

function initializeBootstrapValidation() {
    'use strict'
    
    const forms = document.querySelectorAll('.needs-validation')
    
    Array.from(forms).forEach(form => {
        form.addEventListener('submit', event => {
            // Check custom link validation first
            const linkFields = form.querySelectorAll('input[name="link"], input[name="lwj"], input[name="lrsj"], input[name="lap"]');
            let hasInvalidLinks = false;
            
            linkFields.forEach(field => {
                if (!field.checkValidity()) {
                    hasInvalidLinks = true;
                    field.classList.add('is-invalid');
                } else if (field.value.trim() !== "") {
                    field.classList.add('is-valid');
                }
            });
            
            // Then check standard HTML5 validation
            if (!form.checkValidity() || hasInvalidLinks) {
                event.preventDefault()
                event.stopPropagation()
            }
            
            form.classList.add('was-validated')
        }, false)
    })
}

var curr_count = 0;
document.addEventListener('submit', function(e) {
    const form = e.target;

    // Only intercept submissions for our targeted forms
    const isSubFor = form.classList.contains('sub-form');
    const isUplExe = form.classList.contains('upl-exe');

    if (!isSubFor && !isUplExe) {
        return; // Let standard forms submit normally
    }

    e.preventDefault(); // Stop native submit only for handled forms

    const submitButton = form.querySelector('button[type="submit"]');

    if (submitButton) {
        submitButton.disabled = true;
        submitButton.innerText = "Saving...";
    }

    const formData = new FormData(form);

    // -------------------------------------------------------------
    // FORM TYPE 1: .sub-for
    // -------------------------------------------------------------
    if (isSubFor) {
        fetch(`/save_all_forms/${form_number}`, {
            method: 'POST',
            body: formData,
            headers: { 'X-CSRFToken': csrfToken }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                curr_count++;
                if (submitButton) submitButton.innerText = "Saved Successfully!";
                if (curr_count === formCounter) {
                    window.location.href = '/success';
                }
            } else {
                if (data.from === 'file') {
                    // Update modal content directly without attaching cumulative .on() listeners
                    const $modal = $('#messageModal');
                    $modal.find('#icon').attr('class', 'fa-solid fa-triangle-exclamation text-dark mt-1 me-2');
                    $modal.find('#header').css('background-color', '#FEC901');
                    $modal.find('#modal-title').text('Warning');
                    $modal.find('#message').html(data.message);
                    $modal.modal('show');
                } else {
                    showMessages(data.message, "danger");
                }

                if (submitButton) {
                    submitButton.disabled = false;
                    submitButton.innerText = "Try Again";
                }
            }
        })
        .catch(error => {
            console.error("Error fetching result:", error);
            if (submitButton) {
                submitButton.disabled = false;
                submitButton.innerText = "Try Again";
            }
        });
    }
    // -------------------------------------------------------------
    // FORM TYPE 2: .upl-exe
    // -------------------------------------------------------------
    else if (isUplExe) {
        fetch(`/upload_excel/${form_number}`, {
            method: 'POST',
            body: formData,
            headers: { 'X-CSRFToken': csrfToken }
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                if (submitButton) submitButton.innerText = "Saved Successfully!";
                window.location.href = '/all_forms/' + form_number;
            } else {
                if (submitButton) {
                    submitButton.disabled = false;
                    submitButton.innerText = "Try Again";
                }
                alert(data.error || 'Upload failed.');
            }
        })
        .catch(error => {
            console.error("Error fetching result:", error);
            if (submitButton) {
                submitButton.disabled = false;
                submitButton.innerText = "Try Again";
            }
        });
    }
});