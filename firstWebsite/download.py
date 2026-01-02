import base64
import io

import pandas as pd
from django.forms.models import model_to_dict
from django.http.response import HttpResponse
from django.shortcuts import render

from firstWebsite.modals import Faculty, Student_Directory
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

        else:
            return render(request,'404.html')
    else:
        return render(request, '404.html')