import base64
import io

import openpyxl
import pandas as pd
from django.forms.models import model_to_dict
from django.http.response import HttpResponse
from django.shortcuts import render

from firstWebsite.modals import Faculty, Student_Directory, non_teaching_staff, Faculty_participation_data, mooc_course, \
    awards_and_achievments, events, sponsored_research, research_journal, research_conference, research_book, patents, \
    guided, resource
from firstWebsite.views import session_login_required


@session_login_required
def download_files(request):
    if request.method == "POST":
        if request.POST.get('file_type') == 'excel':
            CHOICES_FIELDS = ['department', 'designation', 'aos', 'hq', 'status', 'role', 'gender']
            files_field = ['profile_picture', 'jr', 'of', 'hdc', 'ss', 'certificate']
            values = request.POST.getlist('optcheck[]')
            result_instance = Faculty.objects.filter(department__in=values,status="R")

            data = []

            # 2. Iterate and process each instance
            for result in result_instance:

                row_dict = model_to_dict(result)

                # b) Dynamically override the code value with the display value
                for field_name in CHOICES_FIELDS:
                    # getattr to call the correct get_FIELDNAME_display() method

                    display_method = getattr(result, f'get_{field_name}_display')

                    row_dict[field_name] = display_method()

                for field in files_field:
                    hyperlink_text = "https://uttkarsh007.pythonanywhere.com/media/" + str(row_dict[field])
                    hyperlink_formula = f'=HYPERLINK("{hyperlink_text}", "View File online")'
                    row_dict[field] = hyperlink_formula

                data.append(row_dict)

            df = pd.DataFrame(data)
            #For CSV
            json_data = df.to_json(orient='records', date_format='iso')
            request.session['csv_data'] = json_data
            #For Excel
            output = io.BytesIO()
            writer = pd.ExcelWriter(output, engine='xlsxwriter')
            df.to_excel(writer,index = False,sheet_name="faculty_report",header=['S.No.','Name','Contact Number','Email','Department','Gender','Address','Employee ID','Role','Status','Desigantion','Area of Specialization','Highest Qualification','University Name(highest degree)','Passing Year of Highest Degree','PAN NO.','Date of birth','Joining Data','Promotion Date','Profile Picture(Link)','Joining Report','Offer Letter','Salary Slip','Highest Degree Certificate','Extra Certificate','PHD pursuing University Name','PHD Date of Registration','Number of research paper'])

            writer.close()
            excel_data = base64.b64encode(output.getvalue())
            request.session['excel_data'] = excel_data.decode('utf-8')
        else:
            return render(request,'404.html')

    elif request.method == "GET":
        if request.GET.get('file_type') == 'excel_repo':
            excel_data = request.session.get('excel_data').encode('utf-8')
            retrieved_excel_data = base64.b64decode(excel_data)
            response = HttpResponse(
                retrieved_excel_data,
                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )
            response['Content-Disposition'] = 'attachment; filename="faculty_report.xlsx"'
            return response

        elif request.GET.get('file_type') == 'excel_dir':
            result_instance = Faculty.objects.all()

            data = [
                {
                    'Name': result.name,
                    'Email': result.email,
                    'Employee ID': result.emp_id,
                    'Department': result.get_department_display(),
                    'Contact Number': result.contact_number,
                    'Status': result.get_status_display()
                }
                for result in result_instance
            ]

            df = pd.DataFrame(data)
            output = io.BytesIO()
            writer = pd.ExcelWriter(output, engine='openpyxl')
            df.to_excel(writer, index=False, sheet_name="faculty_directory")
            writer.close()
            excel_data = output.getvalue()
            response = HttpResponse(
                excel_data,
                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )
            response['Content-Disposition'] = 'attachment; filename="faculty_directory.xlsx"'
            return response

        elif request.GET.get('file_type') == 'excel_stu_dir':
            result_instance = Student_Directory.objects.all()
            data = [
                {
                    'Name': result.name,
                    'Roll No': result.roll_no,
                    'College ID': result.college_id,
                    'Email': result.email,
                    'Student Phone No': result.student_phone_no,
                    'Parent Phone No': result.parent_phone_no,
                    'Address': result.address
                }
                for result in result_instance
            ]

            df = pd.DataFrame(data)
            output = io.BytesIO()
            writer = pd.ExcelWriter(output, engine='openpyxl')
            df.to_excel(writer, index=False, sheet_name="student_directory")
            writer.close()
            excel_data = output.getvalue()
            response = HttpResponse(
                excel_data,
                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )
            response['Content-Disposition'] = 'attachment; filename="student_directory.xlsx"'
            return response

        elif request.GET.get('file_type') == 'csv_repo' or request.GET.get('file_type') == 'csv_dir' or request.GET.get('file_type') == 'csv_stu_dir':
            return render(request,'page_under_construction.html')

        elif request.GET.get('file_type') == 'fdc_dir_data':
            workbook = openpyxl.Workbook()
            default_sheet = workbook.active
            workbook.remove(default_sheet)
            user_type = request.session.get('topLeftBar')

            # --- Non-teaching Staff Details ---
            sheet1 = workbook.create_sheet("1. Non-Teaching Staff Profile")
            headers_1 = ['Timestamp','Email address','Session','Name','Mobile No','Department','Lab No','Designation','Employee ID','Highest Qualification','University Name','Passing Year of Highest degree','Professional Courses','PAN No.','Date of Birth','Joining Date (DD, MM, YY)','Promotion Date ( If any)','The above mentioned information is correct best to my knowledge']

            if user_type == 'ad' or user_type == 'spa':
                headers_1.insert(12,'Higher Degree Certificate(Date of Award)')
                headers_1.insert(18,'Joining Report')
                headers_1.insert(19,'Offer Letter (Appointment Letter)')
                headers_1.insert(20,'Salary Slip (Recently)')
                headers_1.insert(21,'If Awards and recognition received for extension activities (Upload Certificate)')

            sheet1.append(headers_1)

            for item in non_teaching_staff.objects.all():
                # item.higher_degree_certificate, item.joining_date, item.joining_report, item.offer_letter, item.salary_slip, item.certificate,
                row_data = [item.created_at.strftime("%d-%m-%Y %H:%M:%S"), item.email.email, item.get_session_display(),
                               item.name, item.mobile_no, item.get_department_display(), item.Lab_no, item.get_designation_display(),
                               item.emp_id, item.highest_qual, item.university_name, item.pshd,
                               item.professional_course, item.pan_no, item.dob, item.promotion_date,
                               'I Agree']
                if item.joining_report and user_type == 'ad' or user_type == 'spa':
                    item.joining_report = item.joining_report.url
                    row_data.insert(18,item.joining_report)
                elif not item.joining_report and user_type == 'ad' or user_type == 'spa':
                    item.joining_report = "No File"
                    row_data.insert(18, item.joining_report)

                if item.offer_letter and user_type == 'ad' or user_type == 'spa':
                    item.offer_letter = item.offer_letter.url
                    row_data.insert(19,item.offer_letter)
                elif not item.offer_letter and user_type == 'ad' or user_type == 'spa':
                    item.offer_letter = "No File"
                    row_data.insert(19,item.offer_letter)

                if item.higher_degree_certificate and user_type == 'ad' or user_type == 'spa':
                    item.higher_degree_certificate = item.higher_degree_certificate.url
                    row_data.insert(12, item.higher_degree_certificate)
                elif not item.higher_degree_certificate and user_type == 'ad' or user_type == 'spa':
                    item.higher_degree_certificate = "No File"
                    row_data.insert(12, item.higher_degree_certificate)

                if item.salary_slip and user_type == 'ad' or user_type == 'spa':
                    item.salary_slip = item.salary_slip.url
                    row_data.insert(20, item.salary_slip)
                elif not item.salary_slip and user_type == 'ad' or user_type == 'spa':
                    item.salary_slip = "No File"
                    row_data.insert(20, item.salary_slip)

                if item.certificate and user_type == 'ad' or user_type == 'spa':
                    item.certificate = item.certificate.url
                    row_data.insert(21, item.certificate)
                elif not item.certificate and user_type == 'ad' or user_type == 'spa':
                    item.certificate = "No File"
                    row_data.insert(21, item.certificate)

                sheet1.append(row_data)

                if item.joining_report and user_type == 'ad' or user_type == 'spa':
                    cell = sheet1.cell(row=sheet1.max_row, column=19)
                    cell.hyperlink = "https://uttkarsh007.pythonanywhere.com/" + item.joining_report.url
                    cell.style = "Hyperlink"

                if item.offer_letter and user_type == 'ad' or user_type == 'spa':
                    cell = sheet1.cell(row=sheet1.max_row, column=20)
                    cell.hyperlink = "https://uttkarsh007.pythonanywhere.com/" + item.offer_letter.url
                    cell.style = "Hyperlink"


                if item.higher_degree_certificate and user_type == 'ad' or user_type == 'spa':
                    cell = sheet1.cell(row=sheet1.max_row, column=13)
                    cell.hyperlink = "https://uttkarsh007.pythonanywhere.com/" + item.highest_degree_certificate.url
                    cell.style = "Hyperlink"


                if item.salary_slip and user_type == 'ad' or user_type == 'spa':
                    cell = sheet1.cell(row=sheet1.max_row, column=21)
                    cell.hyperlink = "https://uttkarsh007.pythonanywhere.com/" + item.salary_slip.url
                    cell.style = "Hyperlink"


                if item.certificate and user_type == 'ad' or user_type == 'spa':
                    cell = sheet1.cell(row=sheet1.max_row, column=22)
                    cell.hyperlink = "https://uttkarsh007.pythonanywhere.com/" + item.certificate.url
                    cell.style = "Hyperlink"


            # --- Faculty Participartion ---
            sheet2 = workbook.create_sheet("2. Faculty Participation")
            headers_2 = ['Timestamp','Email address','Employee ID','Department','Name of Faculty Memeber','Title of Program','Conference/FDP/ Workshop/Seminar/ STTP','Mode (Online/Offline)','Level','Organizer','Sponsored By','Grant received from SKIT (Yes/No)','From Date','To Date','Session','No. of Days','Proof Enclosed (Yes/No)']
            if user_type == "ad" or user_type == "spa":
                headers_2.append('Upload Certificate/Proof')
            sheet2.append(headers_2)

            for item in Faculty_participation_data.objects.all():
                row_data = [item.created_at.strftime("%d-%m-%Y %H:%M:%S"), item.email.email, item.email.emp_id, item.email.get_department_display(),
                               item.email.name, item.top, item.get_category_display(), item.get_mode_display(),
                               item.get_level_display(), item.organizer, item.sponsors, item.get_approval_display(),
                               item.begi_date.strftime("%d-%m-%Y"), item.end_date.strftime("%d-%m-%Y"), item.get_session_display(),
                               item.no_of_days, item.get_proof_enclosed_display()]
                if item.proof_file and user_type == "ad" or user_type == "spa":
                    proof_file = "https://uttkarsh007.pythonanywhere.com/" + item.proof_file.url
                    row_data.append(proof_file)
                elif not item.proof_file and user_type == "ad" or user_type == "spa":
                    proof_file = "No File"
                    row_data.append(proof_file)

                sheet2.append(row_data)

                if item.proof_file and user_type == 'ad' or user_type == 'spa':
                    cell = sheet2.cell(row=sheet2.max_row, column=18)
                    cell.hyperlink = "https://uttkarsh007.pythonanywhere.com/" + item.proof_file.url
                    cell.style = "Hyperlink"

            # --- 3. MOOCsShort Term Course ---
            sheet3 = workbook.create_sheet("3. MOOCsShort Term Course")
            headers_3 = ['Timestamp', 'Email address', 'Session', 'Name of Faculty Memeber', 'Employee ID' ,'Department',
                           'Type of Course', 'Timeline of course', 'Name of the Course', 'Duration of Course', 'Start Date of Course',
                           'End Date of Course', 'Offering Agency / Organizer', 'Certificate Type', 'Any  category from below ',
                           'Remarks (if any)']
            if user_type == 'ad' or user_type == 'spa':
                headers_3.insert(15,'Upload Certificate/Proof')
            sheet3.append(headers_3)


            for item in mooc_course.objects.all():
                row_data = [item.created_at.strftime("%d-%m-%Y %H:%M:%S"), item.email.email, item.get_session_display(), item.email.name, item.email.emp_id,
                               item.email.get_department_display(),
                               item.get_category_display(), item.timeline, item.noc,
                               item.get_doc_display(),
                               item.begi_date.strftime("%d-%m-%Y"), item.end_date.strftime("%d-%m-%Y"), item.offer, item.get_ctype_display(),
                               item.get_topper_in_display(),
                               item.remarks]
                if item.proof_file and user_type == 'ad' or user_type == 'spa':
                    proof_file = "https://uttkarsh007.pythonanywhere.com/" + item.proof_file.url
                    row_data.insert(15,proof_file)
                elif not item.proof_file and user_type == 'ad' or user_type == 'spa':
                    proof_file = "No File"
                    row_data.insert(15,proof_file)

                sheet3.append(row_data)

                if item.proof_file and user_type == 'ad' or user_type == 'spa':
                    cell = sheet3.cell(row=sheet3.max_row, column=16)
                    cell.hyperlink = "https://uttkarsh007.pythonanywhere.com/" + item.proof_file.url
                    cell.style = "Hyperlink"

            # --- 4. Events Organized by Department ---
            sheet4 = workbook.create_sheet("4Events Organized by Department")
            headers_4 = ['Timestamp', 'Email address', 'Start Date of the Event', 'End Date  the Event ' ,'Event Organized for', 'Type of Event', 'Name of Faculty Coordinator(s)',
                         'Title of the Professional Development Program Organized', 'No. of participants', 'Academic Department/ Cell / Committees/ Labs /COE',
                         'Academic Session', 'Sponsored/Non Sponsored', 'Name of Sponsoring Agency (if Sponsored)', 'Collaboration Details', 'Grant Received (YES/NO)', 'Grant Details',
                         'Association with professional societies for organization of event',
                         'Number of SKIT students participated (Provide list of students with their RTU roll no. & Certificates)s',
                         'Number of staff member participated(Provide list of staff members with  their EMPLOYEE ID & Certificates)',
                         'Event report attached in proper format(YES/NO)', 'Any Other Remark']
            if user_type == 'ad' or user_type == 'spa':
                headers_4.insert(19,'Upload Event Report')
            sheet4.append(headers_4)

            for item in events.objects.all():
                row_data = [item.created_at.strftime("%d-%m-%Y %H:%M:%S"), item.email.email, item.begi_date.strftime("%d-%m-%Y"),
                               item.end_date.strftime("%d-%m-%Y"), item.eof, item.get_category_display(),
                               item.nofc, item.topdpo, item.nop,
                               item.adcc, item.get_session_display(), item.get_ct_display(),
                               item.nosa, item.cd,
                               item.get_gr_display(), item.gd, item.awpsfooe, item.nossp, item.nosmp, item.get_eraipf_display(),
                               item.remarks]
                if item.proof_file and user_type == 'ad' or user_type == 'spa':
                    proof_file = "https://uttkarsh007.pythonanywhere.com/" + item.proof_file.url
                    row_data.insert(19,proof_file)
                elif not item.proof_file and user_type == 'ad' or user_type == 'spa':
                    proof_file = "No File"
                    row_data.insert(19, proof_file)

                sheet4.append(row_data)

                if item.proof_file and user_type == 'ad' or user_type == 'spa':
                    cell = sheet4.cell(row=sheet4.max_row, column=20)
                    cell.hyperlink = "https://uttkarsh007.pythonanywhere.com/" + item.proof_file.url
                    cell.style = "Hyperlink"

            # --- 5. Faculty Awards & Achievement ---
            sheet5 = workbook.create_sheet("5. Faculty Awards & Achievement")
            headers_5 = ['Timestamp', 'Email address', 'Session', 'Faculty Name', 'Employee ID',
                           'Designation', 'Department', 'Name of the Award/Achievement', 'Category','Position / Award For',
                           'Agency/Organization', 'Prize', 'Remark',
                           'All information filled by me is correct and I will submit proof and other related document whenever is asked']
            if user_type == 'ad' or user_type == 'spa':
                headers_5.insert(12,'Upload Award Certificate/Proof')
            sheet5.append(headers_5)

            for item in awards_and_achievments.objects.all():
                row_data = [item.created_at.strftime("%d-%m-%Y %H:%M:%S"), item.email.email, item.get_session_display(),
                               item.email.name, item.email.emp_id, item.email.get_designation_display(), item.email.get_department_display(),
                               item.noaa, item.get_category_display(), item.paf,
                               item.ao, item.prize,
                               item.remark, "I AGREE"]
                if item.proof_file and user_type == 'ad' or user_type == 'spa':
                    proof_file = "https://uttkarsh007.pythonanywhere.com/" + item.proof_file.url
                    row_data.insert(12,proof_file)
                elif not item.proof_file and user_type == 'ad' or user_type == 'spa':
                    proof_file = "No File"
                    row_data.insert(12,proof_file)

                sheet5.append(row_data)

                if item.proof_file and user_type == 'ad' or user_type == 'spa':
                    cell = sheet5.cell(row=sheet5.max_row, column=13)
                    cell.hyperlink = "https://uttkarsh007.pythonanywhere.com/" + item.proof_file.url
                    cell.style = "Hyperlink"

            # --- 6. Sponsored Research/Grant Received/Consultancy ---
            sheet6 = workbook.create_sheet("6. Sponsored Research, Grant")
            headers_6 = ['Timestamp', 'Email address', 'Name of Candidate (PI/Co PI)', 'Employee ID', 'Department',
                           'Category ', ' Name of the funding agency (MSME/DST/CSIR/SERB /Industry etc.)', 'Duration of Project (in Years)',
                           'Amount in Rs.', 'Session in which grant/research project/consultancy received', 'Status']
            if user_type == 'ad' or user_type == 'spa':
                headers_6.append('Upload Proof')

            sheet6.append(headers_6)

            for item in sponsored_research.objects.all():
                row_data = [item.created_at.strftime("%d-%m-%Y %H:%M:%S"), item.email.email, item.email.name,
                               item.email.emp_id, item.email.get_department_display(), item.get_category_display(),
                               item.nofa, item.dop,
                               item.amount, item.get_session_display(), item.get_status_display(),
                               ]
                if item.proof_file and user_type == 'ad' or user_type == 'spa':
                    proof_file = "https://uttkarsh007.pythonanywhere.com/" + item.proof_file.url
                    row_data.append(proof_file)
                elif not item.proof_file and user_type == 'ad' or user_type == 'spa':
                    proof_file = "No File"
                    row_data.append(proof_file)

                sheet6.append(row_data)

                if item.proof_file and user_type == 'ad' or user_type == 'spa':
                    cell = sheet6.cell(row=sheet6.max_row, column=12)
                    cell.hyperlink = "https://uttkarsh007.pythonanywhere.com/" + item.proof_file.url
                    cell.style = "Hyperlink"

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

            for item in research_journal.objects.all():
                row_data = [item.created_at.strftime("%d-%m-%Y %H:%M:%S"), item.email.email, item.email.emp_id,
                               item.noa, item.email.get_department_display(), item.top,
                               item.noj, item.nop, item.vi,
                               item.pn, item.pd, item.get_session_display(),
                               item.isnp, item.isno, item.get_level_display(), item.doi, item.lwj, item.lap, item.lrsj, item.aiop,
                               item.get_index_by_display(), item.get_quartile_display(), item.get_ssa_display(), item.details,
                               ]
                if item.proof_file and user_type == 'ad' or user_type == 'spa':
                    proof_file = "https://uttkarsh007.pythonanywhere.com/" + item.proof_file.url
                    row_data.append(proof_file)
                elif not item.proof_file and user_type == 'ad' or user_type == 'spa':
                    proof_file = "No File"
                    row_data.append(proof_file)

                sheet7.append(row_data)

                if item.proof_file and user_type == 'ad' or user_type == 'spa':
                    cell = sheet7.cell(row=sheet7.max_row, column=25)
                    cell.hyperlink = "https://uttkarsh007.pythonanywhere.com/" + item.proof_file.url
                    cell.style = "Hyperlink"

            # --- 7.2 Conference Publication ---
            sheet8 = workbook.create_sheet("7.2 Conference Publication")
            headers_8 = ['Timestamp', 'Email address', 'Department', 'Employee ID', 'Name of author',
                           'Title of the Conference', 'Title of paper', 'Title of the proceedings of the conference','Level(National/International)', 'ISBN/ISSN number of the proceeding','Name of the Publisher', 'Published Date', 'Session',
                           'DOI', 'Web Link', 'Affiliating Institute at the time of publication', 'Indexed by', 'Is SKIT stuacdent associated?', 'If Yes , Write student(s) details (Program, Branch, RollNo/EnrollNo, Name)']
            if user_type == 'ad' or user_type == 'spa':
                headers_8.append('Upload Full Paper')
            sheet8.append(headers_8)

            for item in research_conference.objects.all():
                row_data = [item.created_at.strftime("%d-%m-%Y %H:%M:%S"), item.email.email, item.email.get_department_display(),
                               item.email.emp_id, item.noa, item.toc,
                               item.top, item.topc, item.get_level_display(),
                               item.isnp, item.nop, item.pd, item.get_session_display(),
                               item.doi, item.lwj, item.aitp,
                               item.get_index_by_display(), item.get_ssa_display(), item.details,
                               ]
                if item.proof_file and user_type == 'ad' or user_type == 'spa':
                    proof_file = "https://uttkarsh007.pythonanywhere.com/" + item.proof_file.url
                    row_data.append(proof_file)
                elif not item.proof_file and user_type == 'ad' or user_type == 'spa':
                    proof_file = "No File"
                    row_data.append(proof_file)

                sheet8.append(row_data)

                if item.proof_file and user_type == 'ad' or user_type == 'spa':
                    cell = sheet8.cell(row=sheet8.max_row, column=20)
                    cell.hyperlink = "https://uttkarsh007.pythonanywhere.com/" + item.proof_file.url
                    cell.style = "Hyperlink"

            # --- 7.3 Book and Book Chapters ---
            sheet9 = workbook.create_sheet("7.3 Book and Book Chapters")
            headers_9 = ['Timestamp', 'Email address', 'Department', 'Employee ID', 'Name of author/editor',
                           'Title of the book', 'Title of chapter Published', 'Level (National/International)',
                           'ISBN', 'Name of the Publisher', 'Published Date', 'Session', 'DOI', 'Web Link', 'Affiliating Institute at the time of publication',
                           'Indexed By', 'Is SKIT student associated', 'If Yes , Write student(s) details (Program, Branch, RollNo/EnrollNo, Name)']
            if user_type == 'ad' or user_type == 'spa':
                headers_9.append('Upload Proof (Book Chapter/Front Page/Document etc.)')
            sheet9.append(headers_9)

            for item in research_book.objects.all():
                row_data = [item.created_at.strftime("%d-%m-%Y %H:%M:%S"), item.email.email, item.email.get_department_display(), item.email.emp_id,
                               item.noa, item.tob,
                               item.top, item.get_level_display(), item.isbn,
                               item.nop, item.pd, item.get_session_display(),
                               item.doi, item.lwj,
                               item.aitp, item.get_index_by_display(), item.get_ssa_display(), item.details]
                if item.proof_file and user_type == 'ad' or user_type == 'spa':
                    proof_file = "https://uttkarsh007.pythonanywhere.com/" + item.proof_file.url
                    row_data.append(proof_file)
                elif not item.proof_file and user_type == 'ad' or user_type == 'spa':
                    proof_file = "No File"
                    row_data.append(proof_file)

                sheet9.append(row_data)

                if item.proof_file and user_type == 'ad' or user_type == 'spa':
                    cell = sheet9.cell(row=sheet9.max_row, column=19)
                    cell.hyperlink = "https://uttkarsh007.pythonanywhere.com/" + item.proof_file.url
                    cell.style = "Hyperlink"

            # --- 7.4 Patents ---
            sheet10 = workbook.create_sheet("7.4 Patents")
            headers_10 = ['Timestamp', 'Email address', 'Session', 'Department', 'Employee ID', 'Name of Faculty',
                           'Status of Patent', 'Application ID', 'Granted ID', 'Type of Patent',
                           'Title of Patent', 'Granted Country', 'Patent Filed Date', 'Publication Date', 'Is SKIT student associated?',
                           'If Yes , Write student(s) details (Program, Branch, RollNo/EnrollNo, Name) ', 'Link']
            if user_type == 'ad' or user_type == 'spa':
                headers_10.append('Upload Proof')
            sheet10.append(headers_10)

            for item in patents.objects.all():
                row_data = [item.created_at.strftime("%d-%m-%Y %H:%M:%S"), item.email.email, item.get_session_display(), item.email.get_department_display(), item.email.emp_id,
                               item.email.name, item.get_sop_display(),
                               item.ag, item.gi, item.get_pg_display(),
                               item.top, item.gc, item.pfd,
                               item.pd.strftime("%d-%m-%Y"), item.get_ssa_display(), item.details,
                               item.link]
                if item.proof_file and user_type == 'ad' or user_type == 'spa':
                    proof_file = "https://uttkarsh007.pythonanywhere.com/" + item.proof_file.url
                    row_data.append(proof_file)
                elif not item.proof_file and user_type == 'ad' or user_type == 'spa':
                    proof_file = "No File"
                    row_data.append(proof_file)

                sheet10.append(row_data)

                if item.proof_file and user_type == 'ad' or user_type == 'spa':
                    cell = sheet10.cell(row=sheet10.max_row, column=18)
                    cell.hyperlink = "https://uttkarsh007.pythonanywhere.com/" + item.proof_file.url
                    cell.style = "Hyperlink"

            # --- 8. M.TechPh.D Guided ---
            sheet11 = workbook.create_sheet("8. M.Tech,Ph.D Guided")
            sheet11.append(['Timestamp', 'Email address','Session', 'Faculty Name', 'Employee ID', 'Department',
                           'Name of the student Guided', 'Program of Student', 'Enrollment Number of Student',
                           'University Roll Number of Student', 'Enrollment Year of Student', 'Title of the Dissertation', 'Supervisor / Co-supervisor', 'Date of Viva-Voce',
                           'Name of external examiner'])

            for item in guided.objects.all():
                sheet11.append([item.created_at.strftime("%d-%m-%Y %H:%M:%S"), item.email.email, item.get_session_display(), item.email.name, item.email.emp_id,
                               item.email.get_department_display(), item.nos,
                               item.get_category_display(), item.ens, item.urns,
                               item.get_eys_display(), item.tod, item.get_visor_display(),
                               item.dov,item.noe])

            # --- 9. M.TechPh.D Guided ---
            sheet12 = workbook.create_sheet("9. Resource Person")
            headers_12 = ['Timestamp', 'Email address','Session', 'Name of Faculty Member', 'Employee ID', 'Department',
                           'Resource Person in', 'Title of Event/ Exam Name', 'Subject Area/Subject Name/Lab Name/Session Name',
                           'Resource Person Type', 'Duration of event (in days)', 'Date From', 'Date to', 'Venue']
            if user_type == 'ad' or user_type == 'spa':
                headers_12.append('Proof (Certificate/Mail)')
            sheet12.append(headers_12)

            for item in resource.objects.all():
                row_data = [item.created_at.strftime("%d-%m-%Y %H:%M:%S"), item.email.email, item.get_session_display(), item.email.name, item.email.emp_id,
                               item.email.get_department_display(), item.get_category_display(),
                               item.toe, item.sa, item.get_rpt_display(),
                               item.doe, item.begi_date.strftime("%d-%m-%Y"), item.end_date.strftime("%d-%m-%Y"),
                               item.venue]
                if item.proof_file and user_type == 'ad' or user_type == 'spa':
                    proof_file = "https://uttkarsh007.pythonanywhere.com/" + item.proof_file.url
                    row_data.append(proof_file)
                elif not item.proof_file and user_type == 'ad' or user_type == 'spa':
                    proof_file = "No File"
                    row_data.append(proof_file)

                sheet12.append(row_data)

                if item.proof_file and user_type == 'ad' or user_type == 'spa':
                    cell = sheet12.cell(row=sheet12.max_row, column=15)
                    cell.hyperlink = "https://uttkarsh007.pythonanywhere.com/" + item.proof_file.url
                    cell.style = "Hyperlink"

            response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = 'attachement; filename=Faculty Data Collection Response Sheet.xlsx'

            workbook.save(response)
            return response

        else:
            return render(request,'404.html')
    else:
        return render(request, '404.html')