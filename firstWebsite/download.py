import base64
import io

import openpyxl
import pandas as pd
from openpyxl.styles import Font
from django.utils import timezone
from django.contrib import messages
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.db.models import F

from firstWebsite.modals import Faculty, non_teaching_staff, Faculty_participation_data, mooc_course, \
    awards_and_achievments, events, sponsored_research, research_journal, research_conference, research_book, patents, \
    guided, resource
from firstWebsite.views import session_login_required

def download_filtered_files(request, model_name, results, file_fields, date_time_fields , date_fields, headers, multi_valued = ""):
    if len(results) > 0:
        # ['department', 'designation', 'aos', 'hq', 'status', 'role', 'gender']
        # ['profile_picture', 'jr', 'of', 'hdc', 'ss', 'certificate']
        # values = request.POST.getlist('optcheck[]')
        # Faculty.objects.filter(department__in=values, status="R")
        result_instance = results

        data = []
        choice_translators = {
            f.name: dict(f.flatchoices)
            for f in model_name._meta.fields if f.choices
        }
        dept_field = Faculty._meta.get_field('department')
        desi_field = Faculty._meta.get_field('designation')
        if dept_field.choices:
            # We map the Department 'name' choices to our annotation key 'dept_name'
            choice_translators['department'] = dict(dept_field.flatchoices)
        if desi_field.choices:
            choice_translators['designation'] = dict(desi_field.flatchoices)
        datetime_fields = date_time_fields
        date_fields = date_fields
        file_fields = file_fields
        multi_valued = multi_valued
        # 2. Iterate and process each instance
        for result in result_instance:
            for field_name, translator_dict in choice_translators.items():
                # Check if this choice field is actually in our current row
                if field_name in result:
                    raw_value = result[field_name]

                    # .get(raw_value, raw_value) means:
                    # "Try to find the display name. If you can't, just leave the raw value alone."
                    result[field_name] = translator_dict.get(raw_value, raw_value)

            for field in file_fields:
                file_path = result.get(field)
                if file_path:
                    hyperlink_text = "https://uttkarsh007.pythonanywhere.com/media/" + file_path
                    hyperlink_formula = f'=HYPERLINK("{hyperlink_text}", "View File Online")'
                    result[field] = hyperlink_formula
                else:
                    text = "No File"
                    result[field] = text

            for field in datetime_fields:
                dt_value = result.get(field)
                if dt_value:
                    # Convert to local time and format as 'dd-mm-yyyy hh:mm:ss'
                    result[field] = timezone.localtime(dt_value).strftime("%d/%m/%Y %H:%M:%S")
                else:
                    # Handle null/empty datetime fields gracefully
                    result[field] = "N/A"

            for field in date_fields:
                date_value = result.get(field)
                if date_value:
                    result[field] = date_value.strftime("%d-%m-%Y")

            if multi_valued != "":
                result[multi_valued] = ", ".join(result.get(multi_valued))

            data.append(result)

        df = pd.DataFrame(data)
        df.rename(columns={'safe_dept': 'dept'}, inplace=True)
        pd.set_option('display.max_columns', None)

        # For CSV
        json_data = df.to_json(orient='records', date_format='iso')
        request.session['csv_data'] = json_data

        # For Excel
        output = io.BytesIO()

        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            # 1. Write the DataFrame to the buffer first
            df.to_excel(writer, index=False, sheet_name="faculty_report")

            # 2. Access the underlying XlsxWriter workbook and worksheet objects
            workbook = writer.book
            worksheet = writer.sheets['faculty_report']

            # ==========================================
            # 3. DEFINE YOUR FONT STYLES (Formats)
            # ==========================================

            # Format for standard data cells
            data_font_format = workbook.add_format({
                'font_name': 'Arial',  # Set your desired font style
                'font_size': 10  # Set your desired font size
            })

            # Format for the header row
            header_font_format = workbook.add_format({
                'font_name': 'Arial',
                'font_size': 11,
                'bold': True
            })

            link_style_format = workbook.add_format({
                'font_color': 'blue',
                'underline': 1
            })

            # ==========================================
            # 4. APPLY FORMATS & AUTOFIT
            # ==========================================

            # Setting default column of collected headers
            initial_headers = df.columns
            df.columns = headers
            # Apply the header format
            # Pandas already wrote the headers, so we iterate through them and overwrite
            # the cells in row 0 with our new custom header format.
            for col_num, col_name in enumerate(df.columns.values):
                worksheet.write(0, col_num, col_name, header_font_format)

            # Apply the data format to all columns
            for col_num in range(len(df.columns)):
                # set_column arguments: (first_col, last_col, width, format)
                # Passing 'None' for width means we aren't setting a manual width yet.
                worksheet.set_column(col_num, col_num, None, data_font_format)

            # Applying link color
            for file_col in file_fields:
                col_idx = initial_headers.get_loc(file_col)
                worksheet.set_column(col_idx, col_idx, None, link_style_format)

            # Autofit the column widths
            # This built-in method calculates the maximum width of the data in each
            # column (including the header) and sizes the column perfectly.
            worksheet.autofit()
        output.seek(0)
        excel_data = base64.b64encode(output.getvalue())
        request.session['excel_data'] = excel_data.decode('utf-8')

@session_login_required
def download_files(request):
    # Data Filteration
    if request.method == "POST":
        form_no = request.POST.get('form_no')
        values = request.POST.getlist('optcheck[]')
        date_time_fields = ['created_at']
        file_fields = ['proof_file']
        if form_no == '1_1': # or '1_1' in forms_to_download
            file_fields = ['jr','of','hdc','ss','certificate']
            date_fields = ['dob','jd','pd','phd_dor']
            result = Faculty.objects.filter(department__in=values, status="R").values(
                'created_at','email','session','name','contact_number','department','designation',
                'aos','emp_id','hq','univ_name','pshd','pan_no','dob','jd','pd','jr','of','ss','hdc','phd_univ',
                'phd_dor','norp','certificate'
            )
            headers_0 = ['Timestamp', 'Email address', 'Session', 'Name', 'Mobile No', 'Department', 'Designation',
                         'Area of specialization', 'Employee ID', 'Highest Qualification', 'University Name',
                         'Passing Year of Highest degree', 'PAN No.', 'Date of Birth',
                         'Joining Date (DD, MM, YY)', 'Promotion Date ( If any)', 'Joining Report', 'Offer Letter (Appointment Letter)',
                         'Salary Slip (Recently)', 'Higher Degree Certificate(Date of Award)',
                         'If PhD pursuing (mention University Name)',
                         'If PhD pursuing (mention Date of Registration)', 'No of Research Paper publication',
                         'If Awards and recognition received for extension activities(Upload Certificate)'
                          ]

            download_filtered_files(request, Faculty, result, file_fields, date_time_fields, date_fields,headers_0)

        elif form_no == '1_2':
            file_fields = ['higher_degree_certificate', 'joining_report', 'offer_letter', 'salary_slip', 'certificate']
            date_fields = ['dob','joining_date','promotion_date']
            multi_select_field = 'professional_course'
            result = non_teaching_staff.objects.all().values(
                'created_at','email','session','name','mobile_no','department','Lab_no',
                'designation','emp_id','highest_qual','university_name','pshd','professional_course',
                'pan_no','dob','joining_date','promotion_date'
            )
            headers_1 = ['Timestamp', 'Email address', 'Session', 'Name', 'Mobile No', 'Department', 'Lab No',
                         'Designation', 'Employee ID','Highest Qualification', 'University Name',
                         'Passing Year of Highest degree', 'Higher Degree Certificate(Date of Award)' ,'Professional Courses', 'PAN No.', 'Date of Birth',
                         'Joining Date (DD, MM, YY)', 'Promotion Date ( If any)', 'Joining Report', 'Offer Letter (Appointment Letter)', 'Salary Slip (Recently)',
                         'If Awards and recognition received for extension activities (Upload Certificate)'
                         ]

            download_filtered_files(request, Faculty, result, file_fields, date_time_fields, date_fields, headers_1, multi_select_field)

        elif form_no == '2':
            date_fields = ['begi_date', 'end_date']
            result = Faculty_participation_data.objects.filter(category__in=values).annotate(
                safe_email=F('email__email'),
                emp_id=F('email__emp_id'),
                department=F('email__department'),
                name=F('email__name')
            ).values(
                'created_at', 'safe_email', 'emp_id', 'department', 'name', 'top', 'category', 'mode','level',
                'organizer', 'sponsors', 'approval', 'begi_date', 'end_date', 'session', 'no_of_days', 'proof_enclosed','proof_file'
            )
            headers_2 = ['Timestamp', 'Email address', 'Employee ID', 'Department', 'Name of Faculty Memeber',
                         'Title of Program', 'Conference/FDP/ Workshop/Seminar/ STTP', 'Mode (Online/Offline)', 'Level',
                         'Organizer', 'Sponsored By', 'Grant received from SKIT (Yes/No)', 'From Date', 'To Date',
                         'Session', 'No. of Days', 'Proof Enclosed (Yes/No)','Upload Certificate/Proof']

            download_filtered_files(request, Faculty_participation_data, result, file_fields, date_time_fields, date_fields, headers_2)

        elif form_no == '3':
            date_fields = ['begi_date', 'end_date']
            result = mooc_course.objects.filter(category__in=values).annotate(
                safe_email=F('email__email'),
                emp_id=F('email__emp_id'),
                department=F('email__department'),
                name=F('email__name')
            ).values(
                'created_at', 'safe_email', 'session', 'name', 'emp_id', 'department', 'category', 'timeline', 'noc',
                'doc', 'begi_date', 'end_date', 'offer', 'ctype', 'topper_in', 'remarks', 'proof_file'
            )
            headers_3 = ['Timestamp', 'Email address', 'Session', 'Name of Faculty Memeber', 'Employee ID',
                         'Department',
                         'Type of Course', 'Timeline of course', 'Name of the Course', 'Duration of Course',
                         'Start Date of Course',
                         'End Date of Course', 'Offering Agency / Organizer', 'Certificate Type',
                         'Any  category from below ',
                         'Remarks (if any)', 'Upload Certificate/Proof']

            download_filtered_files(request, mooc_course, result, file_fields, date_time_fields,
                                    date_fields, headers_3)

        elif form_no == '4':
            date_fields = ['begi_date', 'end_date']
            multi_select_field = 'eof'
            result = events.objects.filter(category__in=values).annotate(
                safe_email=F('email__email'),
                emp_id=F('email__emp_id'),
                department=F('email__department'),
                name=F('email__name')
            ).values(
                'created_at', 'safe_email', 'begi_date', 'end_date', 'eof', 'category', 'nofc', 'topdpo', 'nop',
                'adcc', 'session', 'ct', 'nosa', 'cd', 'gr', 'gd', 'awpsfooe', 'nossp', 'nosmp', 'eraipf', 'remarks', 'proof_file'
            )
            headers_4 = ['Timestamp', 'Email address', 'Start Date of the Event', 'End Date  the Event ',
                         'Event Organized for', 'Type of Event', 'Name of Faculty Coordinator(s)',
                         'Title of the Professional Development Program Organized', 'No. of participants',
                         'Academic Department/ Cell / Committees/ Labs /COE',
                         'Academic Session', 'Sponsored/Non Sponsored',
                         'Name of Sponsoring Agency (if Sponsored)', 'Collaboration Details',
                         'Grant Received (YES/NO)', 'Grant Details',
                         'Association with professional societies for organization of event',
                         'Number of SKIT students participated (Provide list of students with their RTU roll no. & Certificates)s',
                         'Number of staff member participated(Provide list of staff members with  their EMPLOYEE ID & Certificates)',
                         'Event report attached in proper format(YES/NO)', 'Any Other Remark', 'Upload Event Report']

            download_filtered_files(request, events, result, file_fields, date_time_fields,
                                    date_fields, headers_4, multi_select_field)

        elif form_no == '5':
            date_fields = ['ad']
            result = awards_and_achievments.objects.filter(category__in=values).annotate(
                safe_email=F('email__email'),
                emp_id=F('email__emp_id'),
                department=F('email__department'),
                designation=F('email__designation'),
                name=F('email__name')
            ).values(
                'created_at', 'safe_email', 'session', 'name', 'emp_id', 'designation', 'department', 'noaa', 'category', 'paf', 'ao',
                'prize', 'ad', 'remark', 'proof_file'
            )
            headers_5 = ['Timestamp', 'Email address', 'Session', 'Faculty Name', 'Employee ID',
                         'Designation', 'Department', 'Name of the Award/Achievement', 'Category',
                         'Position / Award For',
                         'Agency/Organization', 'Prize', 'Award Date', 'Remark', 'Upload Award Certificate/Proof'
                         ]

            download_filtered_files(request, awards_and_achievments, result, file_fields, date_time_fields,
                                    date_fields, headers_5)

        elif form_no == '6':
            result = sponsored_research.objects.filter(category__in=values).annotate(
                safe_email=F('email__email'),
                emp_id=F('email__emp_id'),
                department=F('email__department'),
                name=F('email__name')
            ).values(
                'created_at', 'safe_email', 'name', 'emp_id', 'department', 'category', 'nofa', 'dop',
                'amount', 'session', 'status', 'proof_file'
            )
            headers_6 = ['Timestamp', 'Email address', 'Name of Candidate (PI/Co PI)', 'Employee ID', 'Department',
                         'Category ', ' Name of the funding agency (MSME/DST/CSIR/SERB /Industry etc.)',
                         'Duration of Project (in Years)',
                         'Amount in Rs.', 'Session in which grant/research project/consultancy received', 'Status', 'Upload Proof']

            download_filtered_files(request, sponsored_research, result, file_fields, date_time_fields,
                                    [], headers_6)

        elif form_no == '7_1':
            date_fields = ['pd']
            result = research_journal.objects.filter(index_by__in=values).annotate(
                safe_email=F('email__email'),
                emp_id=F('email__emp_id'),
                department=F('email__department'),
                name=F('email__name')
            ).values(
                'created_at', 'safe_email', 'emp_id', 'noa', 'department', 'top', 'noj', 'nop', 'vi', 'pn',
                'pd', 'session', 'isnp', 'isno', 'level', 'doi', 'lwj','lap', 'lrsj', 'aiop', 'index_by', 'quartile', 'ssa',
                'details', 'proof_file'
            )
            headers_7_1 = ['Timestamp', 'Email address', 'Employee ID', 'Name of the author', 'Department',
                         'Title of Paper', 'Name of Journal', 'Name of the Publisher', 'Volume, Issue', 'Page No.',
                         'Published Date',
                         'Session', 'ISSN number : Print', 'ISSN number : Online', 'Level (National/International)',
                         'DOI',
                         'Link to website of the Journal',
                         'Link to article/paper/abstract of the article (Direct link to the webpage where the abstract of paper is displayed)',
                         'Link to the recognition in SCOPUS enlistment of the Journal',
                         'Affiliating Institute at the time of publication', 'Indexed by', 'Quartile',
                         'Is SKIT student associated ?',
                         'If Yes , Write student(s) details (Program, Branch, RollNo/EnrollNo, Name)', 'Upload Full Paper']

            download_filtered_files(request, research_journal, result, file_fields, date_time_fields,
                                    date_fields, headers_7_1)

        elif form_no == '7_2':
            date_fields = ['pd']
            result = research_conference.objects.filter(level__in=values).annotate(
                safe_email=F('email__email'),
                emp_id=F('email__emp_id'),
                department=F('email__department'),
                name=F('email__name')
            ).values(
                'created_at', 'safe_email', 'department', 'emp_id', 'noa', 'toc', 'top', 'topc',
                'level', 'isnp', 'nop', 'pd', 'session', 'doi', 'lwj','aitp', 'index_by', 'ssa', 'details', 'proof_file'
            )
            headers_7_2 = ['Timestamp', 'Email address', 'Department', 'Employee ID', 'Name of author',
                         'Title of the Conference', 'Title of paper', 'Title of the proceedings of the conference',
                         'Level(National/International)', 'ISBN/ISSN number of the proceeding', 'Name of the Publisher',
                         'Published Date', 'Session',
                         'DOI', 'Web Link', 'Affiliating Institute at the time of publication', 'Indexed by',
                         'Is SKIT stuacdent associated?',
                         'If Yes , Write student(s) details (Program, Branch, RollNo/EnrollNo, Name)','Upload Full Paper']

            download_filtered_files(request, research_conference, result, file_fields, date_time_fields,
                                    date_fields, headers_7_2)

        elif form_no == '7_3':
            date_fields = ['pd']
            result = research_book.objects.filter(level__in=values).annotate(
                safe_email=F('email__email'),
                emp_id=F('email__emp_id'),
                department=F('email__department'),
                name=F('email__name')
            ).values(
                'created_at', 'safe_email', 'department', 'emp_id', 'noa', 'tob', 'top', 'level',
                'isbn', 'nop', 'pd', 'session', 'doi', 'lwj','aitp', 'index_by', 'ssa', 'details', 'proof_file'
            )
            headers_7_3 = ['Timestamp', 'Email address', 'Department', 'Employee ID', 'Name of author/editor',
                               'Title of the book', 'Title of chapter Published', 'Level (National/International)',
                               'ISBN', 'Name of the Publisher', 'Published Date', 'Session', 'DOI', 'Web Link', 'Affiliating Institute at the time of publication',
                               'Indexed By', 'Is SKIT student associated', 'If Yes , Write student(s) details (Program, Branch, RollNo/EnrollNo, Name)', 'Upload Proof (Book Chapter/Front Page/Document etc.)']

            download_filtered_files(request, research_book, result, file_fields, date_time_fields,
                                    date_fields, headers_7_3)

        elif form_no == '7_4':
            date_fields = ['pd']
            result = patents.objects.filter(pg__in=values).annotate(
                safe_email=F('email__email'),
                emp_id=F('email__emp_id'),
                department=F('email__department'),
                name=F('email__name')
            ).values(
                'created_at', 'safe_email', 'session','department', 'emp_id', 'name', 'sop', 'ag', 'gi',
                'pg', 'top', 'gc', 'pfd', 'pd', 'ssa','details', 'link', 'proof_file'
            )
            headers_7_4 = ['Timestamp', 'Email address', 'Session', 'Department', 'Employee ID', 'Name of Faculty',
                          'Status of Patent', 'Application ID', 'Granted ID', 'Type of Patent',
                          'Title of Patent', 'Granted Country', 'Patent Filed Date', 'Publication Date',
                          'Is SKIT student associated?',
                          'If Yes , Write student(s) details (Program, Branch, RollNo/EnrollNo, Name) ', 'Link', 'Upload Proof']

            download_filtered_files(request, patents, result, file_fields, date_time_fields,
                                    date_fields, headers_7_4)

        elif form_no == '8':
            date_fields = ['dov']
            result = guided.objects.filter(category__in=values).annotate(
                safe_email=F('email__email'),
                emp_id=F('email__emp_id'),
                department=F('email__department'),
                name=F('email__name')
            ).values(
                'created_at', 'safe_email', 'session','name', 'emp_id', 'department', 'nos', 'category', 'ens',
                'urns', 'eys', 'tod', 'visor', 'dov', 'noe'
            )
            headers_8 = ['Timestamp', 'Email address','Session', 'Faculty Name', 'Employee ID', 'Department',
                               'Name of the student Guided', 'Program of Student', 'Enrollment Number of Student',
                               'University Roll Number of Student', 'Enrollment Year of Student', 'Title of the Dissertation', 'Supervisor / Co-supervisor', 'Date of Viva-Voce',
                               'Name of external examiner']

            download_filtered_files(request, guided, result, [], date_time_fields,
                                    date_fields, headers_8)

        elif form_no == '9':
            date_fields = ['begi_date', 'end_date']
            result = resource.objects.filter(category__in=values).annotate(
                safe_email=F('email__email'),
                emp_id=F('email__emp_id'),
                department=F('email__department'),
                name=F('email__name')
            ).values('created_at', 'safe_email', 'session','name', 'emp_id', 'department', 'category', 'toe', 'sa',
                'rpt', 'doe', 'begi_date', 'end_date', 'venue', 'proof_file'
            )
            headers_9 = ['Timestamp', 'Email address','Session', 'Name of Faculty Member', 'Employee ID', 'Department',
                               'Resource Person in', 'Title of Event/ Exam Name', 'Subject Area/Subject Name/Lab Name/Session Name',
                               'Resource Person Type', 'Duration of event (in days)', 'Date From', 'Date to', 'Venue', 'Proof (Certificate/Mail)']

            download_filtered_files(request, resource, result, file_fields, date_time_fields,
                                    date_fields, headers_9)

        return HttpResponse(status=204)

    elif request.method == "GET":
        # Data fetching
        if request.GET.get('file_type') == 'fdc_dir_data_excel_filtered':
            if request.session.get('excel_data'):
                excel_data = request.session.get('excel_data').encode('utf-8')
                retrieved_excel_data = base64.b64decode(excel_data)
                response = HttpResponse(
                    retrieved_excel_data,
                    content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                )
                response['Content-Disposition'] = 'attachment; filename="faculty_report.xlsx"'
                return response
            else:
                messages.error(request, 'Please select at least one filter')
                return redirect('report')

        elif request.GET.get('file_type') == 'fdc_dir_data_excel_full':
            workbook = openpyxl.Workbook()
            default_sheet = workbook.active
            workbook.remove(default_sheet)
            underline_font = Font(color="0563C1", underline="single")
            user_type = request.session.get('topLeftBar')
            forms_to_download = request.GET.getlist('form_id')
            if '1_1' in forms_to_download:
                # --- Faculty Profile Details ---
                sheet0 = workbook.create_sheet("1.1 Faculty Profile Details")
                headers_0 = ['Timestamp', 'Email address', 'Session', 'Name', 'Mobile No', 'Department', 'Designation',
                             'Area of specialization', 'Employee ID', 'Highest Qualification', 'University Name',
                             'Passing Year of Highest degree', 'PAN No.', 'Date of Birth',
                             'Joining Date (DD, MM, YY)', 'Promotion Date ( If any)','If PhD pursuing (mention University Name)',
                             'If PhD pursuing (mention Date of Registration)','No of Research Paper publication','If Awards and recognition received for extension activities(Upload Certificate)'
                             'The above mentioned information is correct best to my knowledge']

                if user_type == 'ad' or user_type == 'spa':
                    headers_0.insert(16, 'Joining Report')
                    headers_0.insert(17, 'Offer Letter (Appointment Letter)')
                    headers_0.insert(18, 'Salary Slip (Recently)')
                    headers_0.insert(19, 'Higher Degree Certificate(Date of Award)')
                    headers_0.insert(23, 'If Awards and recognition received for extension activities (Upload Certificate)')

                sheet0.append(headers_0)
                # for making text bold
                for cell in sheet0[1]:
                    cell.font = Font(name='Arial', size=11, bold=True)

                for item in Faculty.objects.filter(status="R"):
                    row_data = [timezone.localtime(item.created_at).strftime("%d-%m-%Y %H:%M:%S"), item.email,
                                item.get_session_display(),
                                item.name, item.contact_number, item.get_department_display(),
                                item.get_designation_display(), item.get_aos_display(),
                                item.emp_id, item.get_hq_display(), item.univ_name, item.pshd,
                                item.pan_no, item.dob, item.jd,
                                item.pd, item.phd_univ, item.phd_dor, item.norp,
                                'I Agree']
                    if item.jr and (user_type == 'ad' or user_type == 'spa'):
                        joining_report = "https://uttkarsh007.pythonanywhere.com" + item.jr.url
                        row_data.insert(16, joining_report)
                    elif not item.jr and (user_type == 'ad' or user_type == 'spa'):
                        joining_report = "No File"
                        row_data.insert(16, joining_report)

                    if item.of and (user_type == 'ad' or user_type == 'spa'):
                        offer_letter = "https://uttkarsh007.pythonanywhere.com" + item.of.url
                        row_data.insert(17, offer_letter)
                    elif not item.of and (user_type == 'ad' or user_type == 'spa'):
                        offer_letter = "No File"
                        row_data.insert(17, offer_letter)

                    if item.ss and (user_type == 'ad' or user_type == 'spa'):
                        salary_slip = "https://uttkarsh007.pythonanywhere.com" + item.ss.url
                        row_data.insert(18, salary_slip)
                    elif not item.ss and (user_type == 'ad' or user_type == 'spa'):
                        salary_slip = "No File"
                        row_data.insert(18, salary_slip)

                    if item.hdc and (user_type == 'ad' or user_type == 'spa'):
                        higher_degree_certificate = "https://uttkarsh007.pythonanywhere.com" + item.hdc.url
                        row_data.insert(19, higher_degree_certificate)
                    elif not item.hdc and (user_type == 'ad' or user_type == 'spa'):
                        higher_degree_certificate = "No File"
                        row_data.insert(19, higher_degree_certificate)

                    if item.certificate and (user_type == 'ad' or user_type == 'spa'):
                        certificate = "https://uttkarsh007.pythonanywhere.com" + item.certificate.url
                        row_data.insert(23, certificate)
                    elif not item.certificate and (user_type == 'ad' or user_type == 'spa'):
                        certificate = "No File"
                        row_data.insert(23, certificate)

                    sheet0.append(row_data)

                    if item.jr and (user_type == 'ad' or user_type == 'spa'):
                        cell = sheet0.cell(row=sheet0.max_row, column=17)
                        cell.value = "View File Online"
                        cell.hyperlink = "https://uttkarsh007.pythonanywhere.com" + item.jr.url
                        cell.style = "Hyperlink"
                        cell.font = underline_font

                    if item.of and (user_type == 'ad' or user_type == 'spa'):
                        cell = sheet0.cell(row=sheet0.max_row, column=18)
                        cell.value = "View File Online"
                        cell.hyperlink = "https://uttkarsh007.pythonanywhere.com" + item.of.url
                        cell.style = "Hyperlink"
                        cell.font = underline_font

                    if item.ss and (user_type == 'ad' or user_type == 'spa'):
                        cell = sheet0.cell(row=sheet0.max_row, column=19)
                        cell.value = "View File Online"
                        cell.hyperlink = "https://uttkarsh007.pythonanywhere.com" + item.ss.url
                        cell.style = "Hyperlink"
                        cell.font = underline_font

                    if item.hdc and (user_type == 'ad' or user_type == 'spa'):
                        cell = sheet0.cell(row=sheet0.max_row, column=20)
                        cell.value = "View File Online"
                        cell.hyperlink = "https://uttkarsh007.pythonanywhere.com" + item.hdc.url
                        cell.style = "Hyperlink"
                        cell.font = underline_font

                    if item.certificate and (user_type == 'ad' or user_type == 'spa'):
                        cell = sheet0.cell(row=sheet0.max_row, column=24)
                        cell.value = "View File Online"
                        cell.hyperlink = "https://uttkarsh007.pythonanywhere.com" + item.certificate.url
                        cell.style = "Hyperlink"
                        cell.font = underline_font

                for col in sheet0.columns:
                    # selecting the row1
                    header_cell = col[0]
                    header_value = str(col[0].value) if col[0].value else ""
                    max_length = len(header_value)
                    column_letter = col[0].column_letter

                    for cell in col[1:]:
                        if cell.value:
                            val_len = len(str(cell.value))
                            if val_len > max_length:
                                max_length = val_len

                    adjusted_width = max_length + 4

                    sheet0.column_dimensions[column_letter].width = min(adjusted_width, 100)

            if '1_2' in forms_to_download:
                # --- Non-teaching Staff Details ---
                sheet1 = workbook.create_sheet("1.2 Non-Teaching Staff Profile")
                headers_1 = ['Timestamp','Email address','Session','Name','Mobile No','Department','Lab No','Designation','Employee ID','Highest Qualification','University Name',
                             'Passing Year of Highest degree','Professional Courses','PAN No.','Date of Birth','Joining Date (DD, MM, YY)','Promotion Date ( If any)',
                             'The above mentioned information is correct best to my knowledge']

                if user_type == 'ad' or user_type == 'spa':
                    headers_1.insert(12,'Higher Degree Certificate(Date of Award)')
                    headers_1.insert(18,'Joining Report')
                    headers_1.insert(19,'Offer Letter (Appointment Letter)')
                    headers_1.insert(20,'Salary Slip (Recently)')
                    headers_1.insert(21,'If Awards and recognition received for extension activities (Upload Certificate)')

                sheet1.append(headers_1)
                # for making text bold
                for cell in sheet1[1]:
                    cell.font = Font(name='Arial', size=11, bold=True)

                for item in non_teaching_staff.objects.all():
                    row_data = [timezone.localtime(item.created_at).strftime("%d-%m-%Y %H:%M:%S"), item.email.email, item.get_session_display(),
                                   item.name, item.mobile_no, item.get_department_display(), item.Lab_no, item.get_designation_display(),
                                   item.emp_id, item.get_highest_qual_display(), item.university_name, item.pshd,
                                   ", ".join(item.professional_display_list), item.pan_no, item.dob, item.joining_date, item.promotion_date,
                                   'I Agree']
                    if item.higher_degree_certificate and (user_type == 'ad' or user_type == 'spa'):
                        higher_degree_certificate = "https://uttkarsh007.pythonanywhere.com" + item.higher_degree_certificate.url
                        row_data.insert(12, higher_degree_certificate)
                    elif not item.higher_degree_certificate and (user_type == 'ad' or user_type == 'spa'):
                        higher_degree_certificate = "No File"
                        row_data.insert(12, higher_degree_certificate)

                    if item.joining_report and (user_type == 'ad' or user_type == 'spa'):
                        joining_report = "https://uttkarsh007.pythonanywhere.com" + item.joining_report.url
                        row_data.insert(18,joining_report)
                    elif not item.joining_report and (user_type == 'ad' or user_type == 'spa'):
                        joining_report = "No File"
                        row_data.insert(18, joining_report)

                    if item.offer_letter and (user_type == 'ad' or user_type == 'spa'):
                        offer_letter = "https://uttkarsh007.pythonanywhere.com" + item.offer_letter.url
                        row_data.insert(19,offer_letter)
                    elif not item.offer_letter and (user_type == 'ad' or user_type == 'spa'):
                        offer_letter = "No File"
                        row_data.insert(19,offer_letter)

                    if item.salary_slip and (user_type == 'ad' or user_type == 'spa'):
                        salary_slip = "https://uttkarsh007.pythonanywhere.com" + item.salary_slip.url
                        row_data.insert(20, salary_slip)
                    elif not item.salary_slip and (user_type == 'ad' or user_type == 'spa'):
                        salary_slip = "No File"
                        row_data.insert(20, salary_slip)

                    if item.certificate and (user_type == 'ad' or user_type == 'spa'):
                        certificate = "https://uttkarsh007.pythonanywhere.com" + item.certificate.url
                        row_data.insert(21, certificate)
                    elif not item.certificate and (user_type == 'ad' or user_type == 'spa'):
                        certificate = "No File"
                        row_data.insert(21, certificate)

                    sheet1.append(row_data)

                    if item.higher_degree_certificate and (user_type == 'ad' or user_type == 'spa'):
                        cell = sheet1.cell(row=sheet1.max_row, column=13)
                        cell.value = "View File Online"
                        cell.hyperlink = "https://uttkarsh007.pythonanywhere.com" + item.higher_degree_certificate.url
                        cell.style = "Hyperlink"
                        cell.font = underline_font

                    if item.joining_report and (user_type == 'ad' or user_type == 'spa'):
                        cell = sheet1.cell(row=sheet1.max_row, column=19)
                        cell.value = "View File Online"
                        cell.hyperlink = "https://uttkarsh007.pythonanywhere.com" + item.joining_report.url
                        cell.style = "Hyperlink"
                        cell.font = underline_font

                    if item.offer_letter and (user_type == 'ad' or user_type == 'spa'):
                        cell = sheet1.cell(row=sheet1.max_row, column=20)
                        cell.value = "View File Online"
                        cell.hyperlink = "https://uttkarsh007.pythonanywhere.com" + item.offer_letter.url
                        cell.style = "Hyperlink"
                        cell.font = underline_font

                    if item.salary_slip and (user_type == 'ad' or user_type == 'spa'):
                        cell = sheet1.cell(row=sheet1.max_row, column=21)
                        cell.value = "View File Online"
                        cell.hyperlink = "https://uttkarsh007.pythonanywhere.com" + item.salary_slip.url
                        cell.style = "Hyperlink"
                        cell.font = underline_font

                    if item.certificate and (user_type == 'ad' or user_type == 'spa'):
                        cell = sheet1.cell(row=sheet1.max_row, column=22)
                        cell.value = "View File Online"
                        cell.hyperlink = "https://uttkarsh007.pythonanywhere.com" + item.certificate.url
                        cell.style = "Hyperlink"
                        cell.font = underline_font

                for col in sheet1.columns:
                    # selecting the row1
                    header_value = str(col[0].value) if col[0].value else ""
                    max_length = len(header_value)
                    column_letter = col[0].column_letter

                    for cell in col[1:]:
                        if cell.value:
                            val_len = len(str(cell.value))
                            if val_len > max_length:
                                max_length = val_len

                    adjusted_width = max_length + 4

                    sheet1.column_dimensions[column_letter].width = min(adjusted_width, 100)

            if '2' in forms_to_download:
                # --- Faculty Participartion ---
                sheet2 = workbook.create_sheet("2. Faculty Participation")
                headers_2 = ['Timestamp','Email address','Employee ID','Department','Name of Faculty Memeber','Title of Program','Conference/FDP/ Workshop/Seminar/ STTP','Mode (Online/Offline)','Level','Organizer','Sponsored By','Grant received from SKIT (Yes/No)','From Date','To Date','Session','No. of Days','Proof Enclosed (Yes/No)']
                if user_type == "ad" or user_type == "spa":
                    headers_2.append('Upload Certificate/Proof')
                sheet2.append(headers_2)

                for item in Faculty_participation_data.objects.all():
                    row_data = [timezone.localtime(item.created_at).strftime("%d-%m-%Y %H:%M:%S"), item.email.email, item.email.emp_id, item.email.get_department_display(),
                                   item.email.name, item.top, item.get_category_display(), item.get_mode_display(),
                                   item.get_level_display(), item.organizer, item.sponsors, item.get_approval_display(),
                                   item.begi_date.strftime("%d-%m-%Y"), item.end_date.strftime("%d-%m-%Y"), item.get_session_display(),
                                   item.no_of_days, item.get_proof_enclosed_display()]
                    if item.proof_file and (user_type == "ad" or user_type == "spa"):
                        proof_file = "https://uttkarsh007.pythonanywhere.com" + item.proof_file.url
                        row_data.append(proof_file)
                    elif not item.proof_file and (user_type == "ad" or user_type == "spa"):
                        proof_file = "No File"
                        row_data.append(proof_file)

                    sheet2.append(row_data)

                    # for making text bold
                    for cell in sheet2[1]:
                        cell.font = Font(name='Arial', size=11, bold=True)

                    if item.proof_file and (user_type == 'ad' or user_type == 'spa'):
                        cell = sheet2.cell(row=sheet2.max_row, column=18)
                        cell.value = "View File Online"
                        cell.hyperlink = "https://uttkarsh007.pythonanywhere.com" + item.proof_file.url
                        cell.style = "Hyperlink"
                        cell.font = underline_font

                for col in sheet2.columns:
                    # selecting the row1
                    header_cell = col[0]
                    header_value = str(col[0].value) if col[0].value else ""
                    max_length = len(header_value)
                    column_letter = col[0].column_letter

                    for cell in col[1:]:
                        if cell.value:
                            val_len = len(str(cell.value))
                            if val_len > max_length:
                                max_length = val_len

                    adjusted_width = max_length + 4

                    sheet2.column_dimensions[column_letter].width = min(adjusted_width, 100)

            if '3' in forms_to_download:
                # --- 3. MOOCsShort Term Course ---
                sheet3 = workbook.create_sheet("3. MOOC's／Short Term Course")
                headers_3 = ['Timestamp', 'Email address', 'Session', 'Name of Faculty Memeber', 'Employee ID',
                             'Department',
                             'Type of Course', 'Timeline of course', 'Name of the Course', 'Duration of Course',
                             'Start Date of Course',
                             'End Date of Course', 'Offering Agency / Organizer', 'Certificate Type',
                             'Any  category from below ',
                             'Remarks (if any)']
                if user_type == 'ad' or user_type == 'spa':
                    headers_3.insert(15, 'Upload Certificate/Proof')
                sheet3.append(headers_3)

                # for making text bold
                for cell in sheet3[1]:
                    cell.font = Font(name='Arial', size=11, bold=True)

                for item in mooc_course.objects.all():
                    row_data = [timezone.localtime(item.created_at).strftime("%d-%m-%Y %H:%M:%S"), item.email.email,
                                item.get_session_display(), item.email.name, item.email.emp_id,
                                item.email.get_department_display(),
                                item.get_category_display(), item.timeline, item.noc,
                                item.get_doc_display(),
                                item.begi_date.strftime("%d-%m-%Y"), item.end_date.strftime("%d-%m-%Y"), item.offer,
                                item.get_ctype_display(),
                                item.get_topper_in_display(),
                                item.remarks]
                    if item.proof_file and (user_type == 'ad' or user_type == 'spa'):
                        proof_file = "https://uttkarsh007.pythonanywhere.com" + item.proof_file.url
                        row_data.insert(15, proof_file)
                    elif not item.proof_file and (user_type == 'ad' or user_type == 'spa'):
                        proof_file = "No File"
                        row_data.insert(15, proof_file)

                    sheet3.append(row_data)

                    if item.proof_file and (user_type == 'ad' or user_type == 'spa'):
                        cell = sheet3.cell(row=sheet3.max_row, column=16)
                        cell.value = "View File Online"
                        cell.hyperlink = "https://uttkarsh007.pythonanywhere.com" + item.proof_file.url
                        cell.style = "Hyperlink"
                        cell.font = underline_font

                for col in sheet3.columns:
                    # selecting the row1
                    header_cell = col[0]
                    header_value = str(col[0].value) if col[0].value else ""
                    max_length = len(header_value)
                    column_letter = col[0].column_letter

                    for cell in col[1:]:
                        if cell.value:
                            val_len = len(str(cell.value))
                            if val_len > max_length:
                                max_length = val_len

                    adjusted_width = max_length + 4

                    sheet3.column_dimensions[column_letter].width = min(adjusted_width, 100)
            if '4' in forms_to_download:
                # --- 4. Events Organized by Department ---
                sheet4 = workbook.create_sheet("4. Events Organized by Dept")
                headers_4 = ['Timestamp', 'Email address', 'Start Date of the Event', 'End Date  the Event ',
                             'Event Organized for', 'Type of Event', 'Name of Faculty Coordinator(s)',
                             'Title of the Professional Development Program Organized', 'No. of participants',
                             'Academic Department/ Cell / Committees/ Labs /COE',
                             'Academic Session', 'Sponsored/Non Sponsored',
                             'Name of Sponsoring Agency (if Sponsored)', 'Collaboration Details',
                             'Grant Received (YES/NO)', 'Grant Details',
                             'Association with professional societies for organization of event',
                             'Number of SKIT students participated (Provide list of students with their RTU roll no. & Certificates)s',
                             'Number of staff member participated(Provide list of staff members with  their EMPLOYEE ID & Certificates)',
                             'Event report attached in proper format(YES/NO)', 'Any Other Remark']
                if user_type == 'ad' or user_type == 'spa':
                    headers_4.insert(19, 'Upload Event Report')
                sheet4.append(headers_4)

                # for making text bold
                for cell in sheet4[1]:
                    cell.font = Font(name='Arial', size=11, bold=True)

                for item in events.objects.all():
                    row_data = [timezone.localtime(item.created_at).strftime("%d-%m-%Y %H:%M:%S"), item.email.email,
                                item.begi_date.strftime("%d-%m-%Y"),
                                item.end_date.strftime("%d-%m-%Y"), ", ".join(item.eof_display_list),
                                item.get_category_display(),
                                item.nofc, item.topdpo, item.nop,
                                item.adcc, item.get_session_display(), item.get_ct_display(),
                                item.nosa, item.cd,
                                item.get_gr_display(), item.gd, item.awpsfooe, item.nossp, item.nosmp,
                                item.get_eraipf_display(),
                                item.remarks]
                    if item.proof_file and (user_type == 'ad' or user_type == 'spa'):
                        proof_file = "https://uttkarsh007.pythonanywhere.com" + item.proof_file.url
                        row_data.insert(19, proof_file)
                    elif not item.proof_file and (user_type == 'ad' or user_type == 'spa'):
                        proof_file = "No File"
                        row_data.insert(19, proof_file)

                    sheet4.append(row_data)

                    if item.proof_file and (user_type == 'ad' or user_type == 'spa'):
                        cell = sheet4.cell(row=sheet4.max_row, column=20)
                        cell.value = "View File Online"
                        cell.hyperlink = "https://uttkarsh007.pythonanywhere.com" + item.proof_file.url
                        cell.style = "Hyperlink"
                        cell.font = underline_font

                for col in sheet4.columns:
                    # selecting the row1
                    header_cell = col[0]
                    header_value = str(col[0].value) if col[0].value else ""
                    max_length = len(header_value)
                    column_letter = col[0].column_letter

                    for cell in col[1:]:
                        if cell.value:
                            val_len = len(str(cell.value))
                            if val_len > max_length:
                                max_length = val_len

                    adjusted_width = max_length + 4

                    sheet4.column_dimensions[column_letter].width = min(adjusted_width, 100)
            if '5' in forms_to_download:
                # --- 5. Faculty Awards & Achievement ---
                sheet5 = workbook.create_sheet("5. Faculty Awards & Achievement")
                headers_5 = ['Timestamp', 'Email address', 'Session', 'Faculty Name', 'Employee ID',
                               'Designation', 'Department', 'Name of the Award/Achievement', 'Category','Position / Award For',
                               'Agency/Organization', 'Prize', 'Remark',
                               'All information filled by me is correct and I will submit proof and other related document whenever is asked']
                if user_type == 'ad' or user_type == 'spa':
                    headers_5.insert(12,'Upload Award Certificate/Proof')
                sheet5.append(headers_5)

                # for making text bold
                for cell in sheet5[1]:
                    cell.font = Font(name='Arial', size=11, bold=True)

                for item in awards_and_achievments.objects.all():
                    row_data = [timezone.localtime(item.created_at).strftime("%d-%m-%Y %H:%M:%S"), item.email.email, item.get_session_display(),
                                   item.email.name, item.email.emp_id, item.email.get_designation_display(), item.email.get_department_display(),
                                   item.noaa, item.get_category_display(), item.paf,
                                   item.ao, item.prize,
                                   item.remark, "I AGREE"]
                    if item.proof_file and (user_type == 'ad' or user_type == 'spa'):
                        proof_file = "https://uttkarsh007.pythonanywhere.com" + item.proof_file.url
                        row_data.insert(12,proof_file)
                    elif not item.proof_file and (user_type == 'ad' or user_type == 'spa'):
                        proof_file = "No File"
                        row_data.insert(12,proof_file)

                    sheet5.append(row_data)

                    if item.proof_file and (user_type == 'ad' or user_type == 'spa'):
                        cell = sheet5.cell(row=sheet5.max_row, column=13)
                        cell.value = "View File Online"
                        cell.hyperlink = "https://uttkarsh007.pythonanywhere.com" + item.proof_file.url
                        cell.style = "Hyperlink"
                        cell.font = underline_font

                for col in sheet5.columns:
                    # selecting the row1
                    header_cell = col[0]
                    header_value = str(col[0].value) if col[0].value else ""
                    max_length = len(header_value)
                    column_letter = col[0].column_letter

                    for cell in col[1:]:
                        if cell.value:
                            val_len = len(str(cell.value))
                            if val_len > max_length:
                                max_length = val_len

                    adjusted_width = max_length + 4

                    sheet5.column_dimensions[column_letter].width = min(adjusted_width, 100)

            if '6' in forms_to_download:
                # --- 6. Sponsored Research/Grant Received/Consultancy ---
                sheet6 = workbook.create_sheet("6. Sponsored Research, Grant")
                headers_6 = ['Timestamp', 'Email address', 'Name of Candidate (PI/Co PI)', 'Employee ID', 'Department',
                               'Category ', ' Name of the funding agency (MSME/DST/CSIR/SERB /Industry etc.)', 'Duration of Project (in Years)',
                               'Amount in Rs.', 'Session in which grant/research project/consultancy received', 'Status']
                if user_type == 'ad' or user_type == 'spa':
                    headers_6.append('Upload Proof')

                sheet6.append(headers_6)

                # for making text bold
                for cell in sheet6[1]:
                    cell.font = Font(name='Arial', size=11, bold=True)

                for item in sponsored_research.objects.all():
                    row_data = [timezone.localtime(item.created_at).strftime("%d-%m-%Y %H:%M:%S"), item.email.email, item.email.name,
                                   item.email.emp_id, item.email.get_department_display(), item.get_category_display(),
                                   item.nofa, item.dop,
                                   item.amount, item.get_session_display(), item.get_status_display(),
                                   ]
                    if item.proof_file and (user_type == 'ad' or user_type == 'spa'):
                        proof_file = "https://uttkarsh007.pythonanywhere.com" + item.proof_file.url
                        row_data.append(proof_file)
                    elif not item.proof_file and (user_type == 'ad' or user_type == 'spa'):
                        proof_file = "No File"
                        row_data.append(proof_file)

                    sheet6.append(row_data)

                    if item.proof_file and (user_type == 'ad' or user_type == 'spa'):
                        cell = sheet6.cell(row=sheet6.max_row, column=12)
                        cell.value = "View File Online"
                        cell.hyperlink = "https://uttkarsh007.pythonanywhere.com" + item.proof_file.url
                        cell.style = "Hyperlink"
                        cell.font = underline_font

                for col in sheet6.columns:
                    # selecting the row1
                    header_cell = col[0]
                    header_value = str(col[0].value) if col[0].value else ""
                    max_length = len(header_value)
                    column_letter = col[0].column_letter

                    for cell in col[1:]:
                        if cell.value:
                            val_len = len(str(cell.value))
                            if val_len > max_length:
                                max_length = val_len

                    adjusted_width = max_length + 4

                    sheet6.column_dimensions[column_letter].width = min(adjusted_width, 100)
            if '7_1' in forms_to_download:
                # --- 7.1 Research Publication - Journal ---
                sheet7 = workbook.create_sheet("7.1Research Publication-Journal")
                headers_7 = ['Timestamp', 'Email address', 'Employee ID', 'Name of the author', 'Department',
                               'Title of Paper', 'Name of Journal', 'Name of the Publisher', 'Volume, Issue', 'Page No.', 'Published Date',
                               'Session', 'ISSN number : Print', 'ISSN number : Online', 'Level (National/International)', 'DOI',
                               'Link to website of the Journal', 'Link to article/paper/abstract of the article (Direct link to the webpage where the abstract of paper is displayed)',
                               'Link to the recognition in SCOPUS enlistment of the Journal', 'Affiliating Institute at the time of publication', 'Indexed by', 'Quartile',
                               'Is SKIT student associated ?', 'If Yes , Write student(s) details (Program, Branch, RollNo/EnrollNo, Name)']
                if user_type == 'ad' or user_type == 'spa':
                    headers_7.append('Upload Full Paper')
                sheet7.append(headers_7)

                # for making text bold
                for cell in sheet7[1]:
                    cell.font = Font(name='Arial', size=11, bold=True)

                for item in research_journal.objects.all():
                    row_data = [timezone.localtime(item.created_at).strftime("%d-%m-%Y %H:%M:%S"), item.email.email, item.email.emp_id,
                                   item.noa, item.email.get_department_display(), item.top,
                                   item.noj, item.nop, item.vi,
                                   item.pn, item.pd, item.get_session_display(),
                                   item.isnp, item.isno, item.get_level_display(), item.doi, item.lwj, item.lap, item.lrsj, item.aiop,
                                   item.get_index_by_display(), item.get_quartile_display(), item.get_ssa_display(), item.details,
                                   ]
                    if item.proof_file and (user_type == 'ad' or user_type == 'spa'):
                        proof_file = "https://uttkarsh007.pythonanywhere.com" + item.proof_file.url
                        row_data.append(proof_file)
                    elif not item.proof_file and (user_type == 'ad' or user_type == 'spa'):
                        proof_file = "No File"
                        row_data.append(proof_file)

                    sheet7.append(row_data)

                    if item.proof_file and (user_type == 'ad' or user_type == 'spa'):
                        cell = sheet7.cell(row=sheet7.max_row, column=25)
                        cell.value = "View File Online"
                        cell.hyperlink = "https://uttkarsh007.pythonanywhere.com" + item.proof_file.url
                        cell.style = "Hyperlink"
                        cell.font = underline_font

                for col in sheet7.columns:
                    # selecting the row1
                    header_cell = col[0]
                    header_value = str(col[0].value) if col[0].value else ""
                    max_length = len(header_value)
                    column_letter = col[0].column_letter

                    for cell in col[1:]:
                        if cell.value:
                            val_len = len(str(cell.value))
                            if val_len > max_length:
                                max_length = val_len

                    adjusted_width = max_length + 4

                    sheet7.column_dimensions[column_letter].width = min(adjusted_width, 100)
            if '7_2' in forms_to_download:
                # --- 7.2 Conference Publication ---
                sheet8 = workbook.create_sheet("7.2 Conference Publication")
                headers_8 = ['Timestamp', 'Email address', 'Department', 'Employee ID', 'Name of author',
                               'Title of the Conference', 'Title of paper', 'Title of the proceedings of the conference','Level(National/International)', 'ISBN/ISSN number of the proceeding','Name of the Publisher', 'Published Date', 'Session',
                               'DOI', 'Web Link', 'Affiliating Institute at the time of publication', 'Indexed by', 'Is SKIT stuacdent associated?', 'If Yes , Write student(s) details (Program, Branch, RollNo/EnrollNo, Name)']
                if user_type == 'ad' or user_type == 'spa':
                    headers_8.append('Upload Full Paper')
                sheet8.append(headers_8)

                # for making text bold
                for cell in sheet8[1]:
                    cell.font = Font(name='Arial', size=11, bold=True)

                for item in research_conference.objects.all():
                    row_data = [timezone.localtime(item.created_at).strftime("%d-%m-%Y %H:%M:%S"), item.email.email, item.email.get_department_display(),
                                   item.email.emp_id, item.noa, item.toc,
                                   item.top, item.topc, item.get_level_display(),
                                   item.isnp, item.nop, item.pd, item.get_session_display(),
                                   item.doi, item.lwj, item.aitp,
                                   item.index_by, item.get_ssa_display(), item.details,
                                   ]
                    if item.proof_file and (user_type == 'ad' or user_type == 'spa'):
                        proof_file = "https://uttkarsh007.pythonanywhere.com" + item.proof_file.url
                        row_data.append(proof_file)
                    elif not item.proof_file and (user_type == 'ad' or user_type == 'spa'):
                        proof_file = "No File"
                        row_data.append(proof_file)

                    sheet8.append(row_data)

                    if item.proof_file and (user_type == 'ad' or user_type == 'spa'):
                        cell = sheet8.cell(row=sheet8.max_row, column=20)
                        cell.value = "View File Online"
                        cell.hyperlink = "https://uttkarsh007.pythonanywhere.com" + item.proof_file.url
                        cell.style = "Hyperlink"
                        cell.font = underline_font

                for col in sheet8.columns:
                    # selecting the row1
                    header_cell = col[0]
                    header_value = str(col[0].value) if col[0].value else ""
                    max_length = len(header_value)
                    column_letter = col[0].column_letter

                    for cell in col[1:]:
                        if cell.value:
                            val_len = len(str(cell.value))
                            if val_len > max_length:
                                max_length = val_len

                    adjusted_width = max_length + 4

                    sheet8.column_dimensions[column_letter].width = min(adjusted_width, 100)
            if '7_3' in forms_to_download:
                # --- 7.3 Book and Book Chapters ---
                sheet9 = workbook.create_sheet("7.3 Book and Book Chapters")
                headers_9 = ['Timestamp', 'Email address', 'Department', 'Employee ID', 'Name of author/editor',
                               'Title of the book', 'Title of chapter Published', 'Level (National/International)',
                               'ISBN', 'Name of the Publisher', 'Published Date', 'Session', 'DOI', 'Web Link', 'Affiliating Institute at the time of publication',
                               'Indexed By', 'Is SKIT student associated', 'If Yes , Write student(s) details (Program, Branch, RollNo/EnrollNo, Name)']
                if user_type == 'ad' or user_type == 'spa':
                    headers_9.append('Upload Proof (Book Chapter/Front Page/Document etc.)')
                sheet9.append(headers_9)

                # for making text bold
                for cell in sheet9[1]:
                    cell.font = Font(name='Arial', size=11, bold=True)

                for item in research_book.objects.all():
                    row_data = [timezone.localtime(item.created_at).strftime("%d-%m-%Y %H:%M:%S"), item.email.email, item.email.get_department_display(), item.email.emp_id,
                                   item.noa, item.tob,
                                   item.top, item.get_level_display(), item.isbn,
                                   item.nop, item.pd, item.get_session_display(),
                                   item.doi, item.lwj,
                                   item.aitp, item.index_by, item.get_ssa_display(), item.details]
                    if item.proof_file and (user_type == 'ad' or user_type == 'spa'):
                        proof_file = "https://uttkarsh007.pythonanywhere.com" + item.proof_file.url
                        row_data.append(proof_file)
                    elif not item.proof_file and (user_type == 'ad' or user_type == 'spa'):
                        proof_file = "No File"
                        row_data.append(proof_file)

                    sheet9.append(row_data)

                    if item.proof_file and (user_type == 'ad' or user_type == 'spa'):
                        cell = sheet9.cell(row=sheet9.max_row, column=19)
                        cell.value = "View File Online"
                        cell.hyperlink = "https://uttkarsh007.pythonanywhere.com" + item.proof_file.url
                        cell.style = "Hyperlink"
                        cell.font = underline_font

                for col in sheet9.columns:
                    # selecting the row1
                    header_cell = col[0]
                    header_value = str(col[0].value) if col[0].value else ""
                    max_length = len(header_value)
                    column_letter = col[0].column_letter

                    for cell in col[1:]:
                        if cell.value:
                            val_len = len(str(cell.value))
                            if val_len > max_length:
                                max_length = val_len

                    adjusted_width = max_length + 4

                    sheet9.column_dimensions[column_letter].width = min(adjusted_width, 100)
            if '7_4' in forms_to_download:
                # --- 7.4 Patents ---
                sheet10 = workbook.create_sheet("7.4 Patents")
                headers_10 = ['Timestamp', 'Email address', 'Session', 'Department', 'Employee ID', 'Name of Faculty',
                               'Status of Patent', 'Application ID', 'Granted ID', 'Type of Patent',
                               'Title of Patent', 'Granted Country', 'Patent Filed Date', 'Publication Date', 'Is SKIT student associated?',
                               'If Yes , Write student(s) details (Program, Branch, RollNo/EnrollNo, Name) ', 'Link']
                if user_type == 'ad' or user_type == 'spa':
                    headers_10.append('Upload Proof')
                sheet10.append(headers_10)

                # for making text bold
                for cell in sheet10[1]:
                    cell.font = Font(name='Arial', size=11, bold=True)

                for item in patents.objects.all():
                    row_data = [timezone.localtime(item.created_at).strftime("%d-%m-%Y %H:%M:%S"), item.email.email, item.get_session_display(), item.email.get_department_display(), item.email.emp_id,
                                   item.email.name, item.get_sop_display(),
                                   item.ag, item.gi, item.get_pg_display(),
                                   item.top, item.gc, item.pfd,
                                   item.pd.strftime("%d-%m-%Y"), item.get_ssa_display(), item.details,
                                   item.link]
                    if item.proof_file and (user_type == 'ad' or user_type == 'spa'):
                        proof_file = "https://uttkarsh007.pythonanywhere.com" + item.proof_file.url
                        row_data.append(proof_file)
                    elif not item.proof_file and (user_type == 'ad' or user_type == 'spa'):
                        proof_file = "No File"
                        row_data.append(proof_file)

                    sheet10.append(row_data)

                    if item.proof_file and (user_type == 'ad' or user_type == 'spa'):
                        cell = sheet10.cell(row=sheet10.max_row, column=18)
                        cell.value = "View File Online"
                        cell.hyperlink = "https://uttkarsh007.pythonanywhere.com" + item.proof_file.url
                        cell.style = "Hyperlink"
                        cell.font = underline_font

                for col in sheet10.columns:
                    # selecting the row1
                    header_cell = col[0]
                    header_value = str(col[0].value) if col[0].value else ""
                    max_length = len(header_value)
                    column_letter = col[0].column_letter

                    for cell in col[1:]:
                        if cell.value:
                            val_len = len(str(cell.value))
                            if val_len > max_length:
                                max_length = val_len

                    adjusted_width = max_length + 4

                    sheet10.column_dimensions[column_letter].width = min(adjusted_width, 100)
            if '8' in forms_to_download:
                # --- 8. M.TechPh.D Guided ---
                sheet11 = workbook.create_sheet("8. M.Tech,Ph.D Guided")
                sheet11.append(['Timestamp', 'Email address','Session', 'Faculty Name', 'Employee ID', 'Department',
                               'Name of the student Guided', 'Program of Student', 'Enrollment Number of Student',
                               'University Roll Number of Student', 'Enrollment Year of Student', 'Title of the Dissertation', 'Supervisor / Co-supervisor', 'Date of Viva-Voce',
                               'Name of external examiner'])

                # for making text bold
                for cell in sheet11[1]:
                    cell.font = Font(bold=True)

                for item in guided.objects.all():
                    sheet11.append([timezone.localtime(item.created_at).strftime("%d-%m-%Y %H:%M:%S"), item.email.email, item.get_session_display(), item.email.name, item.email.emp_id,
                                   item.email.get_department_display(), item.nos,
                                   item.get_category_display(), item.ens, item.urns,
                                   item.get_eys_display(), item.tod, item.get_visor_display(),
                                   item.dov,item.noe])

                for col in sheet11.columns:
                    # selecting the row1
                    header_cell = col[0]
                    header_value = str(col[0].value) if col[0].value else ""
                    max_length = len(header_value)
                    column_letter = col[0].column_letter

                    for cell in col[1:]:
                        if cell.value:
                            val_len = len(str(cell.value))
                            if val_len > max_length:
                                max_length = val_len

                    adjusted_width = max_length + 4

                    sheet11.column_dimensions[column_letter].width = min(adjusted_width, 100)
            if '9' in forms_to_download:
                # --- 9. M.TechPh.D Guided ---
                sheet12 = workbook.create_sheet("9. Resource Person")
                headers_12 = ['Timestamp', 'Email address','Session', 'Name of Faculty Member', 'Employee ID', 'Department',
                               'Resource Person in', 'Title of Event/ Exam Name', 'Subject Area/Subject Name/Lab Name/Session Name',
                               'Resource Person Type', 'Duration of event (in days)', 'Date From', 'Date to', 'Venue']
                if user_type == 'ad' or user_type == 'spa':
                    headers_12.append('Proof (Certificate/Mail)')
                sheet12.append(headers_12)

                # for making text bold
                for cell in sheet12[1]:
                    cell.font = Font(name='Arial', size=11, bold=True)

                for item in resource.objects.all():
                    row_data = [timezone.localtime(item.created_at).strftime("%d-%m-%Y %H:%M:%S"), item.email.email, item.get_session_display(), item.email.name, item.email.emp_id,
                                   item.email.get_department_display(), item.get_category_display(),
                                   item.toe, item.sa, item.get_rpt_display(),
                                   item.doe, item.begi_date.strftime("%d-%m-%Y"), item.end_date.strftime("%d-%m-%Y"),
                                   item.venue]
                    if item.proof_file and (user_type == 'ad' or user_type == 'spa'):
                        proof_file = "https://uttkarsh007.pythonanywhere.com" + item.proof_file.url
                        row_data.append(proof_file)
                    elif not item.proof_file and (user_type == 'ad' or user_type == 'spa'):
                        proof_file = "No File"
                        row_data.append(proof_file)

                    sheet12.append(row_data)

                    if item.proof_file and (user_type == 'ad' or user_type == 'spa'):
                        cell = sheet12.cell(row=sheet12.max_row, column=15)
                        cell.value = "View File Online"
                        cell.hyperlink = "https://uttkarsh007.pythonanywhere.com" + item.proof_file.url
                        cell.style = "Hyperlink"
                        cell.font = underline_font

                for col in sheet12.columns:
                    # selecting the row1
                    header_cell = col[0]
                    header_value = str(col[0].value) if col[0].value else ""
                    max_length = len(header_value)
                    column_letter = col[0].column_letter

                    for cell in col[1:]:
                        if cell.value:
                            val_len = len(str(cell.value))
                            if val_len > max_length:
                                max_length = val_len

                    adjusted_width = max_length + 4

                    sheet12.column_dimensions[column_letter].width = min(adjusted_width, 100)

            response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = 'attachement; filename=Faculty Data Collection Response Sheet.xlsx'

            workbook.save(response)
            return response

        elif request.GET.get('file_type') == 'fdc_dir_data_csv_filtered':
            if request.session.get('csv_data'):
                df = pd.read_json(request.session.get('csv_data'), orient='records')

                # 3. Create the proper CSV response
                response = HttpResponse(content_type='text/csv')
                response['Content-Disposition'] = 'attachment; filename="faculty_report.csv"'

                # 4. Write to response
                # noinspection PyTypeChecker
                df.to_csv(path_or_buf=response, index=False)
                return response
            else:
                messages.error(request, 'Please select at least one filter')
                return redirect('report')

        elif request.GET.get('file_type') == 'fdc_dir_data_csv_full':
            return render(request,'page_under_construction.html')

        else:
            return render(request,'404.html')
    else:
        return render(request, '404.html')