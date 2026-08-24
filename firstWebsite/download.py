import base64
import io
import zipfile
import os
import re

import openpyxl
import pandas as pd
from openpyxl.styles import Font
from django.utils import timezone
from django.contrib import messages
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.db.models import F
from django.db.models import Q

from MyFirstDjangoWebsite import settings
from firstWebsite.modals import Faculty, non_teaching_staff, Faculty_participation_data, mooc_course, \
    awards_and_achievments, events, sponsored_research, research_journal, research_conference, research_book, patents, \
    guided, resource, department, doc, sponsors, designation, area_of_spe, highest_qual, accept, level, mode, category, \
    medals, pertopper, eof_choices, mapped_sdgs, status, index_by, quartile, type_of_patent, status_of_patent, \
    enrollmentYear, survillance, resource_person_type, designation_non_tech, ProfessionalCourseChoices, forms, \
    generate_session_choices
from firstWebsite.decorators import session_login_required

forms_value_to_label = {
    '1_1' : 'faculty_profile_report',
    '1_2' : 'non_teaching_staff_report',
    '2' : 'faculty_participation_report',
    '3' : 'mooc_short_term_course_report',
    '4' : 'events_organized_report',
    '5' : 'faculty_awards_report',
    '6' : 'sponsored_research_report',
    '7_1' : 'research_journal_report',
    '7_2' : 'research_conference_report',
    '7_3' : 'research_book_report',
    '7_4' : 'patents_report',
    '8' : 'mtech_phd_report',
    '9' : 'resource_person_report',
}

ori_forms_value_to_label = {choice.value: choice.label for choice in forms}

def download_filtered_files(request, model_name, results, file_fields, date_time_fields, date_fields, headers, form_no):
    try:

        if len(results) > 0:
            # ['department', 'designation', 'aos', 'hq', 'status', 'role', 'gender']
            # ['profile_picture', 'jr', 'of', 'hdc', 'ss', 'certificate']
            # values = request.POST.getlist('optcheck[]')
            # Faculty.objects.filter(department__in=values, status="R")
            result_instance = results

            data = []
            choice_translators = {
                f.name: dict(f.flatchoices) for f in model_name._meta.fields if f.choices
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
            file_paths_links = []
            # 2. Iterate and process each instance
            for result in result_instance:
                for field_name, translator_dict in choice_translators.items():
                    # Check if this choice field is actually in our current row
                    # To get the label value corresponding to it's value
                    if field_name in result:
                        raw_value = result[field_name]
                        if isinstance(raw_value, list) and len(raw_value) > 0:
                            result[field_name] = ", ".join([translator_dict.get(value, value) for value in raw_value])

                        elif isinstance(raw_value, str) and "," in raw_value:
                            result[field_name] = model_name.map_sdg_display_list

                        # .get(raw_value, raw_value) means:
                        # "Try to find the display name. If you can't, just leave the raw value alone."
                        else:
                            result[field_name] = translator_dict.get(raw_value, raw_value)

                for field in file_fields:
                    file_path = result.get(field)
                    if file_path:
                        hyperlink_text = "https://uttkarsh007.pythonanywhere.com/media/" + file_path
                        file_paths_links.append(os.path.join(settings.MEDIA_ROOT,file_path))
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

                data.append(result)

            df = pd.DataFrame(data)
            df.rename(columns={'safe_dept': 'dept'}, inplace=True)
            pd.set_option('display.max_columns', None)

            # For CSV
            json_data = df.to_json(orient='records', date_format='iso')
            request.session['csv_data'] = json_data

            # Zip Folder
            zip_buffer = io.BytesIO()

            with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
                # For Excel
                excel_buffer = io.BytesIO()
                with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
                    # 1. Write the DataFrame to the buffer first
                    sheet_name = forms_value_to_label.get(form_no, 'new_report')
                    df.to_excel(writer, index=False, sheet_name=sheet_name)

                    # 2. Access the underlying XlsxWriter workbook and worksheet objects
                    workbook = writer.book
                    worksheet = writer.sheets[sheet_name]

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

                excel_buffer.seek(0)
                filename = ori_forms_value_to_label.get(form_no, form_no)
                clean_name = re.sub(r'[ /-]','_', str(filename))
                zip_file.writestr(f"{clean_name}_report.xlsx", excel_buffer.getvalue())

                # print("File path links list looks like: ", file_paths_links)
                for file_path in file_paths_links:
                    try:
                        zip_file.write(file_path, arcname=f'{clean_name}Files/{os.path.basename(file_path)}')
                    except Exception as e:
                        print("File Not Found: ",e)

            zip_bytes = zip_buffer.getvalue()
            request.session['zip_data'] = base64.b64encode(zip_bytes).decode('utf-8')
            request.session['curr_form_no'] = form_no
            return True, 'All Ok'
    except Exception as e:
        return False, str(e)

# def download_session_backup(request, headers, form_no_list, session_filter):
#     workbook = openpyxl.Workbook()
#     default_sheet = workbook.active
#     workbook.remove(default_sheet)
#     underline_font = Font(color="0563C1", underline="single")



# Fetching code values to filter out data
sponsors_label_to_value = {choice.label: choice.value for choice in sponsors}
department_label_to_value = {choice.label: choice.value for choice in department}
desgination_label_to_value = {choice.label: choice.value for choice in designation}
area_of_spe_label_to_value = {choice.label: choice.value for choice in area_of_spe}
high_qual_label_to_value = {choice.label: choice.value for choice in highest_qual}
accept_label_to_value = {choice.label: choice.value for choice in accept}
level_label_to_value = {choice.label: choice.value for choice in level}
mode_label_to_value = {choice.label: choice.value for choice in mode}
category_label_to_value = {choice.label: choice.value for choice in category}
doc_label_to_value = {choice.label: choice.value for choice in doc}
medals_label_to_value = {choice.label: choice.value for choice in medals}
pertopper_label_to_value = {choice.label: choice.value for choice in pertopper}
eof_choices_label_to_value = {choice.label: choice.value for choice in eof_choices}
mapped_sdg_label_to_value = {choice.label: choice.value for choice in mapped_sdgs}
status_label_to_value = {choice.label: choice.value for choice in status}
index_by_label_to_value = {choice.label: choice.value for choice in index_by}
quartile_label_to_value = {choice.label: choice.value for choice in quartile}
type_of_patent_label_to_value = {choice.label: choice.value for choice in type_of_patent}
status_of_patent_label_to_value = {choice.label: choice.value for choice in status_of_patent}
enrollementYear_label_to_value = {choice.label: choice.value for choice in enrollmentYear}
survillance_label_to_value = {choice.label: choice.value for choice in survillance}
resource_person_type_label_to_value = {choice.label: choice.value for choice in resource_person_type}
designation_non_tech_label_to_value = {choice.label: choice.value for choice in designation_non_tech}
professinal_course_label_to_value = {choice.label: choice.value for choice in ProfessionalCourseChoices}

@session_login_required
def download_files(request, back_up_data=False):
    # Data Filteration
    if request.method == "POST":
        form_no = request.POST.get('form_no')

        dept_label_to_value = {choice.label: choice.value for choice in department}
        # Basic Filters
        basic_filtering_values = request.POST.getlist('optcheck_filter[]')
        session_filter = request.POST.get('session_filter')
        if request.POST.get('emp_id_filter') != '':
            emp_id_filter = int(request.POST.get('emp_id_filter'))
        else:
            emp_id_filter = 0
        email_filter = request.POST.get('email_filter')
        name_filter = request.POST.get('name_filter')
        department_filter = request.POST.getlist('department_filter[]')
        department_filter = [dept_label_to_value.get(item, item) for item in department_filter]
        designation_filter = request.POST.getlist('designation_filter[]')
        designation_filter = [desgination_label_to_value.get(item, item) for item in designation_filter]

        filter_mappings = {
            'session': session_filter,
            'email__department__in': department_filter,
            'email__emp_id': emp_id_filter,
            'email__email__icontains': email_filter,
            'email__name__icontains': name_filter,
        }

        query = Q()

        date_time_fields = ['created_at']
        file_fields = ['proof_file']
        if form_no == '1_1': # or '1_1' in forms_to_download

            file_fields = ['jr','of','hdc','ss','certificate']
            date_fields = ['dob','jd','pd','phd_dor']

            filter_mappings = {
                'session': session_filter,
                'department__in': department_filter,
                'emp_id': emp_id_filter,
                'email__icontains': email_filter,
                'name__icontains': name_filter,
                'designation__in': designation_filter,
                'status': "R"
            }

            for lookup, val in filter_mappings.items():
                if val and val != 0:  # Only add to query if val is not None, '', or []
                    query &= Q(**{lookup: val})

            result = Faculty.objects.filter(query).values(
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

            success, message = download_filtered_files(request, Faculty, result, file_fields, date_time_fields, date_fields,headers_0,form_no)
            return JsonResponse({'success': success, 'message': message}, safe=False)

        elif form_no == '1_2':
            file_fields = ['higher_degree_certificate', 'joining_report', 'offer_letter', 'salary_slip', 'certificate']
            date_fields = ['dob','joining_date','promotion_date']

            # Addditional Filters
            highest_filter = request.POST.getlist('highest_filter[]')
            highest_filter = [high_qual_label_to_value.get(item, item) for item in highest_filter]
            professional_course_filter = request.POST.getlist('professional_course_filter[]')
            professional_course_filter = [professinal_course_label_to_value.get(item, item) for item in professional_course_filter]

            filter_mappings = {
                'session': session_filter,
                'department__in': department_filter,
                'emp_id': emp_id_filter,
                'email__icontains': email_filter,
                'name__icontains': name_filter,
                'designation__in': designation_filter,
                'highest_qual__in': highest_filter,
                'professional_course__icontains': professional_course_filter
            }

            for lookup, val in filter_mappings.items():
                if lookup == 'professional_course__icontains' and isinstance(val, list):
                    grouped_query = Q()
                    for v in val:
                        grouped_query |= Q(professional_course__icontains=f'"{v}"')
                    query &= grouped_query
                elif val and val != 0:  # Only add to query if val is not None, '', or []
                    query &= Q(**{lookup: val})

            result = non_teaching_staff.objects.filter(query).values(
                'created_at','email','session','name','mobile_no','department','Lab_no',
                'designation','emp_id','highest_qual','university_name','pshd','professional_course',
                'pan_no','dob','joining_date','promotion_date'
            )
            headers_1 = ['Timestamp', 'Email address', 'Session', 'Name', 'Mobile No', 'Department', 'Lab No',
                         'Designation', 'Employee ID','Highest Qualification', 'University Name',
                         'Passing Year of Highest degree', 'Higher Degree Certificate(Date of Award)' ,'Professional Courses', 'PAN No.', 'Date of Birth',
                         'Joining Date (DD, MM, YY)', 'Promotion Date (If any)', 'Joining Report', 'Offer Letter (Appointment Letter)', 'Salary Slip (Recently)',
                         'If Awards and recognition received for extension activities (Upload Certificate)'
                         ]

            success, message = download_filtered_files(request, non_teaching_staff, result, file_fields, date_time_fields, date_fields, headers_1, form_no)
            return JsonResponse({'success': success, 'message': message}, safe=False)

        elif form_no == '2':
            date_fields = ['begi_date', 'end_date']

            # Additional Filters
            mode_filter = request.POST.getlist('mode_filter[]')
            mode_filter = [mode_label_to_value.get(item, item) for item in mode_filter]
            level_filter = request.POST.getlist('level_filter[]')
            level_filter = [level_label_to_value.get(item, item) for item in level_filter]
            grant_filter = request.POST.getlist('grant_filter[]')
            grant_filter = [accept_label_to_value.get(item, item) for item in grant_filter]
            basic_filtering_values = [category_label_to_value.get(item, item) for item in basic_filtering_values]


            filter_mappings['category__in'] = basic_filtering_values
            filter_mappings['mode__in'] = mode_filter
            filter_mappings['level__in'] = level_filter
            filter_mappings['approval__in'] = grant_filter

            for lookup, val in filter_mappings.items():
                if val and val != 0:  # Only add to query if val is not None, '', or []
                    query &= Q(**{lookup: val})

            result = Faculty_participation_data.objects.filter(query).annotate(
                safe_email=F('email__email'),
                emp_id=F('email__emp_id'),
                department=F('email__department'),
                name=F('email__name')
            ).values(
                'created_at', 'safe_email', 'emp_id', 'department', 'name', 'top', 'category', 'mode','level',
                'organizer', 'sponsors', 'approval', 'begi_date', 'end_date', 'session', 'no_of_days', 'proof_enclosed','proof_file'
            )
            headers_2 = ['Timestamp', 'Email address', 'Employee ID', 'Department', 'Name of Faculty Memeber',
                         'Title of the Program', 'Conference/FDP/ Workshop/Seminar/ STTP', 'Mode (Offline/Online)', 'Level',
                         'Organizer', 'Sponsored By', 'Grant received from SKIT (Yes/No)', 'From Date', 'To Date',
                         'Session', 'No. of Days', 'Proof Enclosed (Yes/No)','Upload Certificate/Proof']

            success, message = download_filtered_files(request, Faculty_participation_data, result, file_fields, date_time_fields, date_fields, headers_2, form_no)
            return JsonResponse({'success': success, 'message': message}, safe=False)

        elif form_no == '3':
            date_fields = ['begi_date', 'end_date']

            # Additional Filters
            duration_filter = request.POST.getlist('duration_filter[]')
            duration_filter = [doc_label_to_value.get(item, item) for item in duration_filter]
            certificate_filter = request.POST.getlist('certificate_filter[]')
            certificate_filter = [medals_label_to_value.get(item, item) for item in certificate_filter]
            topper_filter = request.POST.getlist('topper_filter[]')
            topper_filter = [pertopper_label_to_value.get(item, item) for item in topper_filter]
            basic_filtering_values = [category_label_to_value.get(item, item) for item in basic_filtering_values]

            filter_mappings['category__in'] = basic_filtering_values
            filter_mappings['doc__in'] = duration_filter
            filter_mappings['ctype__in'] = certificate_filter
            filter_mappings['topper_in__in'] = topper_filter

            for lookup, val in filter_mappings.items():
                if val and val != 0:  # Only add to query if val is not None, '', or []
                    query &= Q(**{lookup: val})

            result = mooc_course.objects.filter(query).annotate(
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
                         'Any category from below ',
                         'Remark (if any)', 'Upload Certificate']

            success, message = download_filtered_files(request, mooc_course, result, file_fields, date_time_fields,
                                    date_fields, headers_3, form_no)
            return JsonResponse({'success': success, 'message': message}, safe=False)

        elif form_no == '4':
            date_fields = ['begi_date', 'end_date']

            # Additional Filters
            event_org_for_filter = request.POST.getlist('event_org_for_filter[]')
            event_org_for_filter = [eof_choices_label_to_value.get(item, item) for item in event_org_for_filter]
            spo_non_spo_filter = request.POST.getlist('spo_non_spo_filter[]')
            spo_non_spo_filter = [sponsors_label_to_value.get(item, item) for item in spo_non_spo_filter]
            grant_filter = request.POST.getlist('grant_filter[]')
            grant_filter = [accept_label_to_value.get(item, item) for item in grant_filter]
            map_filter = request.POST.getlist('map_filter[]')
            map_filter = [mapped_sdg_label_to_value.get(item, item) for item in map_filter]
            basic_filtering_values = [category_label_to_value.get(item, item) for item in basic_filtering_values]

            filter_mappings['category__in'] = basic_filtering_values
            filter_mappings['eof__icontains'] = event_org_for_filter
            filter_mappings['ct__in'] = spo_non_spo_filter
            filter_mappings['gr__in'] = grant_filter
            filter_mappings['map_sdg__icontains'] = map_filter

            for lookup, val in filter_mappings.items():
                if (lookup == 'eof__icontains' or lookup == 'map_sdg__icontains') and isinstance(val, list):
                    grouped_query = Q()
                    for v in val:
                        if lookup == 'map_sdg__icontains':
                            # Since values are separated by commas, the key v (e.g., 'SDG1') can only exist in four possible positions within the database string:

                            # 1. Only value: 'SDG1'
                            # 2. At the start: 'SDG1,SDG2'
                            # 3. At the end: 'SDG5,SDG1'
                            # 4. In the middle: 'SDG3,SDG1,SDG5'

                            # To match 'SDG1' without matching 'SDG17', check for commas around the boundaries:
                            sdg_exact_query = (
                                    Q(map_sdg=v) |  # 1. Only item
                                    Q(map_sdg__startswith=f"{v},") |  # 2. First item in list
                                    Q(map_sdg__endswith=f",{v}") |  # 3. Last item in list
                                    Q(map_sdg__contains=f",{v},")  # 4. Middle item in list
                            )
                            grouped_query |= sdg_exact_query
                        elif lookup == 'eof__icontains':
                            grouped_query |= Q(eof__icontains=f'"{v}"')

                    query &= grouped_query
                elif val and val != 0:  # Only add to query if val is not None, '', or []
                    query &= Q(**{lookup: val})

            result = events.objects.filter(query).annotate(
                safe_email=F('email__email'),
                emp_id=F('email__emp_id'),
                department=F('email__department'),
                name=F('email__name')
            ).values(
                'created_at', 'safe_email', 'begi_date', 'end_date', 'eof', 'category', 'nofc', 'topdpo', 'nop',
                'adcc', 'session', 'ct', 'nosa', 'cd', 'gr', 'gd', 'actual_expenditure', 'awpsfooe', 'nossp', 'nosmp', 'map_sdg','eraipf', 'remarks', 'proof_file'
            )
            headers_4 = ['Timestamp', 'Email address', 'Start Date of the Event', 'End Date of the Event',
                         'Event Organized for', 'Type of Event', 'Name of Faculty Coordinator(s)',
                         'Title of the Professional Development Program Organized', 'No. of participants',
                         'Academic Department/ Cell / Committees/ Labs /COE',
                         'Academic Session', 'Sponsored/Non Sponsored',
                         'Name of Sponsoring Agency (if Sponsored)', 'Collaboration Details',
                         'Grant Received (YES/NO)', 'Grant Details', 'Actual Expenditure',
                         'Association with professional societies for organization of event',
                         'Number of SKIT students participated (Provide list of students with their RTU roll no. & Certificates)',
                         'Number of staff member participated(Provide list of staff members with  their EMPLOYEE ID & Certificates)',
                         'Mapped SDGs', 'Event report attached in proper format(YES/NO)',
                         'Any Other Remark', 'Upload Event Report']

            success, message = download_filtered_files(request, events, result, file_fields, date_time_fields,
                                    date_fields, headers_4, form_no)

            return JsonResponse({'success': success, 'message': message}, safe=False)

        elif form_no == '5':
            date_fields = ['ad']

            basic_filtering_values = [category_label_to_value.get(item, item) for item in basic_filtering_values]

            filter_mappings['category__in'] = basic_filtering_values
            filter_mappings['designation__in'] = designation_filter

            for lookup, val in filter_mappings.items():
                if val and val != 0:  # Only add to query if val is not None, '', or []
                    query &= Q(**{lookup: val})

            result = awards_and_achievments.objects.filter(query).annotate(
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
                         'Agency/Organization', 'Prize', 'Date of Award', 'Remark', 'Upload Award Certificate/Proof'
                         ]

            success, message = download_filtered_files(request, awards_and_achievments, result, file_fields, date_time_fields,
                                    date_fields, headers_5, form_no)
            return JsonResponse({'success': success, 'message': message}, safe=False)

        elif form_no == '6':

            # Additional Filters
            status_filter = request.POST.getlist('status_filter[]')
            status_filter = [status_label_to_value.get(item, item) for item in status_filter]
            basic_filtering_values = [category_label_to_value.get(item, item) for item in basic_filtering_values]

            filter_mappings['status__in'] = status_filter
            filter_mappings['category__in'] = basic_filtering_values

            for lookup, val in filter_mappings.items():
                if val and val != 0:  # Only add to query if val is not None, '', or []
                    query &= Q(**{lookup: val})

            result = sponsored_research.objects.filter(query).annotate(
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

            success, message = download_filtered_files(request, sponsored_research, result, file_fields, date_time_fields,
                                    [], headers_6, form_no)
            return JsonResponse({'success': success, 'message': message}, safe=False)

        elif form_no == '7_1':
            date_fields = ['pd']

            # Additional Filters
            level_filter = request.POST.getlist('level_filter[]')
            level_filter = [level_label_to_value.get(item, item) for item in level_filter]
            quartile_filter = request.POST.getlist('quartile_filter[]')
            quartile_filter = [quartile_label_to_value.get(item, item) for item in quartile_filter]
            ssa_filter = request.POST.getlist('ssa_filter[]')
            ssa_filter = [accept_label_to_value.get(item, item) for item in ssa_filter]

            filter_mappings['level__in'] = level_filter
            filter_mappings['quartile__in'] = quartile_filter
            filter_mappings['ssa__in'] = ssa_filter
            basic_filtering_values = [index_by_label_to_value.get(item, item) for item in basic_filtering_values]
            filter_mappings['index_by__in'] = basic_filtering_values

            for lookup, val in filter_mappings.items():
                if val and val != 0:  # Only add to query if val is not None, '', or []
                    query &= Q(**{lookup: val})

            result = research_journal.objects.filter(query).annotate(
                safe_email=F('email__email'),
                emp_id=F('email__emp_id'),
                department=F('email__department'),
                name=F('email__name')
            ).values(
                'created_at', 'safe_email', 'emp_id', 'noa', 'department', 'top', 'noj', 'nop', 'vi', 'pn',
                'pd', 'session', 'isnp', 'isno', 'level', 'doi', 'lwj','lap', 'lrsj', 'aiop', 'index_by', 'quartile', 'ssa',
                'details', 'proof_file'
            )
            headers_7_1 = ['Timestamp', 'Email address', 'Employee ID', 'Name of the author(s)', 'Department',
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

            success, message = download_filtered_files(request, research_journal, result, file_fields, date_time_fields,
                                    date_fields, headers_7_1, form_no)
            return JsonResponse({'success': success, 'message': message}, safe=False)

        elif form_no == '7_2':
            date_fields = ['pd']

            # Additional Filter
            ssa_filter = request.POST.getlist('ssa_filter[]')
            ssa_filter = [accept_label_to_value.get(item, item) for item in ssa_filter]

            filter_mappings['ssa__in'] = ssa_filter
            basic_filtering_values = [level_label_to_value.get(item, item) for item in basic_filtering_values]
            filter_mappings['level__in'] = basic_filtering_values

            for lookup, val in filter_mappings.items():
                if val and val != 0:  # Only add to query if val is not None, '', or []
                    query &= Q(**{lookup: val})

            result = research_conference.objects.filter(query).annotate(
                safe_email=F('email__email'),
                emp_id=F('email__emp_id'),
                department=F('email__department'),
                name=F('email__name')
            ).values(
                'created_at', 'safe_email', 'department', 'emp_id', 'noa', 'toc', 'top', 'topc',
                'level', 'isnp', 'nop', 'pd', 'session', 'doi', 'lwj','aitp', 'index_by', 'ssa', 'details', 'proof_file'
            )
            headers_7_2 = ['Timestamp', 'Email address', 'Department', 'Employee ID', 'Name of author(s)',
                         'Title of the Conference', 'Title of paper', 'Title of the proceedings of the conference',
                         'Level(National/International)', 'ISBN/ISSN number of the proceeding', 'Name of the Publisher',
                         'Published Date', 'Session',
                         'DOI', 'Web Link', 'Affiliating Institute at the time of publication', 'Indexed by',
                         'Is SKIT student associated?',
                         'If Yes , Write student(s) details (Program, Branch, RollNo/EnrollNo, Name)','Upload Full Paper']

            success, message = download_filtered_files(request, research_conference, result, file_fields, date_time_fields,
                                    date_fields, headers_7_2, form_no)
            return JsonResponse({'success': success, 'message': message}, safe=False)

        elif form_no == '7_3':
            date_fields = ['pd']

            # Addtional Filter
            ssa_filter = request.POST.getlist('ssa_filter[]')
            ssa_filter = [accept_label_to_value.get(item, item) for item in ssa_filter]
            basic_filtering_values = [level_label_to_value.get(item, item) for item in basic_filtering_values]

            filter_mappings['level__in'] = basic_filtering_values
            filter_mappings['ssa__in'] = ssa_filter

            for lookup, val in filter_mappings.items():
                if val and val != 0:  # Only add to query if val is not None, '', or []
                    query &= Q(**{lookup: val})

            result = research_book.objects.filter(query).annotate(
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

            success, message = download_filtered_files(request, research_book, result, file_fields, date_time_fields,
                                    date_fields, headers_7_3, form_no)
            return JsonResponse({'success': success, 'message': message}, safe=False)

        elif form_no == '7_4':
            date_fields = ['pd']

            # Additional Filter
            status_filter = request.POST.getlist('status_filter[]')
            status_filter = [status_of_patent_label_to_value.get(item, item) for item in status_filter]
            ssa_filter = request.POST.getlist('ssa_filter[]')
            ssa_filter = [accept_label_to_value.get(item, item) for item in ssa_filter]
            basic_filtering_values = [type_of_patent_label_to_value.get(item, item) for item in basic_filtering_values]

            filter_mappings['pg__in'] = basic_filtering_values
            filter_mappings['ssa__in'] = ssa_filter
            filter_mappings['sop__in'] = status_filter

            for lookup, val in filter_mappings.items():
                if val and val != 0:  # Only add to query if val is not None, '', or []
                    query &= Q(**{lookup: val})

            result = patents.objects.filter(query).annotate(
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

            success, message = download_filtered_files(request, patents, result, file_fields, date_time_fields,
                                    date_fields, headers_7_4, form_no)
            return JsonResponse({'success': success, 'message': message}, safe=False)

        elif form_no == '8':
            date_fields = ['dov']

            # Addtional Filter
            eys_filter = request.POST.getlist('eys_filter[]')
            eys_filter = [enrollementYear_label_to_value.get(item, item) for item in eys_filter]
            visor_filter = request.POST.getlist('visor_filter[]')
            visor_filter = [survillance_label_to_value.get(item, item) for item in visor_filter]
            basic_filtering_values = [category_label_to_value.get(item, item) for item in basic_filtering_values]

            filter_mappings['category__in'] = basic_filtering_values
            filter_mappings['eys__in'] = eys_filter
            filter_mappings['visor__in'] = visor_filter

            for lookup, val in filter_mappings.items():
                if val and val != 0:  # Only add to query if val is not None, '', or []
                    query &= Q(**{lookup: val})

            result = guided.objects.filter(query).annotate(
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

            success, message = download_filtered_files(request, guided, result, [], date_time_fields,
                                    date_fields, headers_8, form_no)
            return JsonResponse({'success': success, 'message': message}, safe=False)

        elif form_no == '9':
            date_fields = ['begi_date', 'end_date']

            # Additional Filter
            rpt_filter = request.POST.getlist('rpt_filter[]')
            rpt_filter = [resource_person_type_label_to_value.get(item, item) for item in rpt_filter]
            basic_filtering_values = [category_label_to_value.get(item, item) for item in basic_filtering_values]


            filter_mappings['category__in'] = basic_filtering_values
            filter_mappings['rpt__in'] = rpt_filter

            for lookup, val in filter_mappings.items():
                if val and val != 0:  # Only add to query if val is not None, '', or []
                    query &= Q(**{lookup: val})

            result = resource.objects.filter(query).annotate(
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

            success, message = download_filtered_files(request, resource, result, file_fields, date_time_fields,
                                    date_fields, headers_9, form_no)
            return JsonResponse({'success': success, 'message': message}, safe=False)

        return JsonResponse({'success': True, 'message': 'All Ok'})

    elif request.method == "GET":
        # Data fetching
        if request.GET.get('file_type') == 'fdc_dir_data_zip_filtered':
            if request.session.get('zip_data'):
                zip_data = request.session.get('zip_data').encode('utf-8')
                retrieved_zip_data = base64.b64decode(zip_data)
                response = HttpResponse(
                    retrieved_zip_data,
                    content_type='application/zip'
                )
                curr_form_no = request.session.get('curr_form_no')
                filename = ori_forms_value_to_label.get(curr_form_no, curr_form_no)
                response['Content-Disposition'] = f'attachment; filename="{filename}_report.zip"'
                return response
            else:
                messages.error(request, 'Please select at least one filter')
                return redirect('report')

        elif request.GET.get('file_type') == 'fdc_dir_data_excel_full' or back_up_data:
            # For Excel
            workbook = openpyxl.Workbook()
            default_sheet = workbook.active
            workbook.remove(default_sheet)
            underline_font = Font(color="0563C1", underline="single")
            user_type = request.session.get('topLeftBar')
            forms_to_download = request.GET.getlist('form_id')
            mastersheet_session_filter =  [session[0] for session in generate_session_choices()]
            # print("MasterSheet filter are: ",mastersheet_session_filter)
            session_filter = request.GET.get('session_filter', 'mastersheet')
            query = Q()
            if session_filter == 'mastersheet':
                for session in mastersheet_session_filter:
                    query |= Q(session=session)
                filename = "Faculty Data Collection Response"
            else:
                query = Q(session=session_filter)
                filename = session_filter

            print("Query is: ",query)

            response = HttpResponse(
                content_type='application/zip')
            response['Content-Disposition'] = f'attachment; filename={filename}.zip'

            zip_buffer = io.BytesIO()
            with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_ref:

                if '1_1' in forms_to_download or back_up_data:
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

                    file_path_links = []

                    custom_query = Q(status="R")
                    if session_filter == 'mastersheet':
                        grouped_query = Q()
                        for session in mastersheet_session_filter:
                            grouped_query |= Q(session=session)
                        custom_query &= grouped_query
                    else:
                        custom_query = Q(session=session_filter)

                    for item in Faculty.objects.filter(custom_query):
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
                            file_path_links.append(item.jr.path)
                        elif not item.jr and (user_type == 'ad' or user_type == 'spa'):
                            joining_report = "No File"
                            row_data.insert(16, joining_report)

                        if item.of and (user_type == 'ad' or user_type == 'spa'):
                            offer_letter = "https://uttkarsh007.pythonanywhere.com" + item.of.url
                            row_data.insert(17, offer_letter)
                            file_path_links.append(item.of.path)
                        elif not item.of and (user_type == 'ad' or user_type == 'spa'):
                            offer_letter = "No File"
                            row_data.insert(17, offer_letter)

                        if item.ss and (user_type == 'ad' or user_type == 'spa'):
                            salary_slip = "https://uttkarsh007.pythonanywhere.com" + item.ss.url
                            row_data.insert(18, salary_slip)
                            file_path_links.append(item.ss.path)
                        elif not item.ss and (user_type == 'ad' or user_type == 'spa'):
                            salary_slip = "No File"
                            row_data.insert(18, salary_slip)

                        if item.hdc and (user_type == 'ad' or user_type == 'spa'):
                            higher_degree_certificate = "https://uttkarsh007.pythonanywhere.com" + item.hdc.url
                            row_data.insert(19, higher_degree_certificate)
                            file_path_links.append(item.hdc.path)
                        elif not item.hdc and (user_type == 'ad' or user_type == 'spa'):
                            higher_degree_certificate = "No File"
                            row_data.insert(19, higher_degree_certificate)

                        if item.certificate and (user_type == 'ad' or user_type == 'spa'):
                            certificate = "https://uttkarsh007.pythonanywhere.com" + item.certificate.url
                            row_data.insert(23, certificate)
                            file_path_links.append(item.certificate.path)
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

                    for file_path in file_path_links:
                        try:
                            zip_ref.write(file_path, arcname=f'Faculty Profile Details Files/{file_path.split('\\')[-2]}/{os.path.basename(file_path).replace("\\", "/")}')
                        except Exception as e:
                            print("File not Found: ",e)

                if '1_2' in forms_to_download or back_up_data:
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

                    file_path_links = []
                    for item in non_teaching_staff.objects.filter(query):
                        row_data = [timezone.localtime(item.created_at).strftime("%d-%m-%Y %H:%M:%S"), item.email.email, item.get_session_display(),
                                       item.name, item.mobile_no, item.get_department_display(), item.Lab_no, item.get_designation_display(),
                                       item.emp_id, item.get_highest_qual_display(), item.university_name, item.pshd,
                                       ", ".join(item.professional_display_list), item.pan_no, item.dob, item.joining_date, item.promotion_date,
                                       'I Agree']
                        if item.higher_degree_certificate and (user_type == 'ad' or user_type == 'spa'):
                            higher_degree_certificate = "https://uttkarsh007.pythonanywhere.com" + item.higher_degree_certificate.url
                            row_data.insert(12, higher_degree_certificate)
                            file_path_links.append(item.higher_degree_certificate.path)
                        elif not item.higher_degree_certificate and (user_type == 'ad' or user_type == 'spa'):
                            higher_degree_certificate = "No File"
                            row_data.insert(12, higher_degree_certificate)

                        if item.joining_report and (user_type == 'ad' or user_type == 'spa'):
                            joining_report = "https://uttkarsh007.pythonanywhere.com" + item.joining_report.url
                            row_data.insert(18,joining_report)
                            file_path_links.append(item.joining_report.path)
                        elif not item.joining_report and (user_type == 'ad' or user_type == 'spa'):
                            joining_report = "No File"
                            row_data.insert(18, joining_report)

                        if item.offer_letter and (user_type == 'ad' or user_type == 'spa'):
                            offer_letter = "https://uttkarsh007.pythonanywhere.com" + item.offer_letter.url
                            row_data.insert(19,offer_letter)
                            file_path_links.append(item.offer_letter.path)
                        elif not item.offer_letter and (user_type == 'ad' or user_type == 'spa'):
                            offer_letter = "No File"
                            row_data.insert(19,offer_letter)

                        if item.salary_slip and (user_type == 'ad' or user_type == 'spa'):
                            salary_slip = "https://uttkarsh007.pythonanywhere.com" + item.salary_slip.url
                            row_data.insert(20, salary_slip)
                            file_path_links.append(item.salary_slip.path)
                        elif not item.salary_slip and (user_type == 'ad' or user_type == 'spa'):
                            salary_slip = "No File"
                            row_data.insert(20, salary_slip)

                        if item.certificate and (user_type == 'ad' or user_type == 'spa'):
                            certificate = "https://uttkarsh007.pythonanywhere.com" + item.certificate.url
                            row_data.insert(21, certificate)
                            file_path_links.append(item.certificate.path)
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

                    for file_path in file_path_links:
                        try:
                            zip_ref.write(file_path, arcname=f'Non-Teaching Staff Profile Details Files/{file_path.split('\\')[-2]}/{os.path.basename(file_path).replace("\\","/")}')
                        except Exception as e:
                            print("File not Found: ",e)

                if '2' in forms_to_download or back_up_data:
                    # --- Faculty Participartion ---
                    sheet2 = workbook.create_sheet("2. Faculty Participation")
                    headers_2 = ['Timestamp','Email address','Employee ID','Department','Name of Faculty Memeber','Title of the Program','Conference/FDP/ Workshop/Seminar/ STTP','Mode (Offline/Online)','Level','Organizer','Sponsored By','Grant received from SKIT (Yes/No)','From Date','To Date','Session','No. of Days','Proof Enclosed (Yes/No)']
                    if user_type == "ad" or user_type == "spa":
                        headers_2.append('Upload Certificate/Proof')
                    sheet2.append(headers_2)

                    file_path_links = []
                    for item in Faculty_participation_data.objects.filter(query):
                        row_data = [timezone.localtime(item.created_at).strftime("%d-%m-%Y %H:%M:%S"), item.email.email, item.email.emp_id, item.email.get_department_display(),
                                       item.email.name, item.top, item.get_category_display(), item.get_mode_display(),
                                       item.get_level_display(), item.organizer, item.sponsors, item.get_approval_display(),
                                       item.begi_date.strftime("%d-%m-%Y"), item.end_date.strftime("%d-%m-%Y"), item.get_session_display(),
                                       item.no_of_days, item.get_proof_enclosed_display()]
                        if item.proof_file and (user_type == "ad" or user_type == "spa"):
                            proof_file = "https://uttkarsh007.pythonanywhere.com" + item.proof_file.url
                            row_data.append(proof_file)
                            file_path_links.append(item.proof_file.path)
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

                    for file_path in file_path_links:
                        try:
                            zip_ref.write(file_path, arcname=f'Faculty Participation Files/{os.path.basename(file_path)}')
                        except Exception as e:
                            print("File not Found: ",e)

                if '3' in forms_to_download or back_up_data:
                    # --- 3. MOOCsShort Term Course ---
                    sheet3 = workbook.create_sheet("3. MOOC's／Short Term Course")
                    headers_3 = ['Timestamp', 'Email address', 'Session', 'Name of Faculty Memeber', 'Employee ID',
                                 'Department',
                                 'Type of Course', 'Timeline of course', 'Name of the Course', 'Duration of Course',
                                 'Start Date of Course',
                                 'End Date of Course', 'Offering Agency / Organizer', 'Certificate Type',
                                 'Any  category from below ',
                                 'Remark (if any)']
                    if user_type == 'ad' or user_type == 'spa':
                        headers_3.insert(15, 'Upload Certificate')
                    sheet3.append(headers_3)

                    # for making text bold
                    for cell in sheet3[1]:
                        cell.font = Font(name='Arial', size=11, bold=True)

                    file_path_links = []
                    for item in mooc_course.objects.filter(query):
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
                            file_path_links.append(item.proof_file.path)
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

                    for file_path in file_path_links:
                        try:
                            zip_ref.write(file_path, arcname=f"MOOC's／Short Term Course／Course Completion Files/{os.path.basename(file_path)}")
                        except Exception as e:
                            print("File not Found: ",e)

                if '4' in forms_to_download or back_up_data:
                    # --- 4. Events Organized by Department ---
                    sheet4 = workbook.create_sheet("4. Events Organized by Dept")
                    headers_4 = ['Timestamp', 'Email address', 'Start Date of the Event', 'End Date of the Event ',
                                 'Event Organized for', 'Type of Event', 'Name of Faculty Coordinator(s)',
                                 'Title of the Professional Development Program Organized', 'No. of participants',
                                 'Academic Department/ Cell / Committees/ Labs /COE',
                                 'Academic Session', 'Sponsored/Non Sponsored',
                                 'Name of Sponsoring Agency (if Sponsored)', 'Collaboration Details',
                                 'Grant Received (YES/NO)', 'Grant Details', 'Actual Expenditure',
                                 'Association with professional societies for organization of event',
                                 'Number of SKIT students participated (Provide list of students with their RTU roll no. & Certificates)',
                                 'Number of staff member participated(Provide list of staff members with  their EMPLOYEE ID & Certificates)',
                                 'Mapped SDGs', 'Event report attached in proper format(YES/NO)', 'Any Other Remark']

                    if user_type == 'ad' or user_type == 'spa':
                        headers_4.insert(19, 'Upload Event Report')
                    sheet4.append(headers_4)

                    # for making text bold
                    for cell in sheet4[1]:
                        cell.font = Font(name='Arial', size=11, bold=True)

                    file_path_links = []
                    for item in events.objects.filter(query):
                        row_data = [timezone.localtime(item.created_at).strftime("%d-%m-%Y %H:%M:%S"), item.email.email,
                                    item.begi_date.strftime("%d-%m-%Y"),
                                    item.end_date.strftime("%d-%m-%Y"), ", ".join(item.eof_display_list),
                                    item.get_category_display(),
                                    item.nofc, item.topdpo, item.nop,
                                    item.adcc, item.get_session_display(), item.get_ct_display(),
                                    item.nosa, item.cd,
                                    item.get_gr_display(), item.gd, item.actual_expenditure, item.awpsfooe, item.nossp, item.nosmp, ", ".join(item.map_sdg),
                                    item.get_eraipf_display(),
                                    item.remarks]
                        if item.proof_file and (user_type == 'ad' or user_type == 'spa'):
                            proof_file = "https://uttkarsh007.pythonanywhere.com" + item.proof_file.url
                            row_data.insert(19, proof_file)
                            file_path_links.append(item.proof_file.path)
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

                    for file_path in file_path_links:
                        try:
                            zip_ref.write(file_path, arcname=f'Events Organized by Department Files/{os.path.basename(file_path)}')
                        except Exception as e:
                            print("File not Found: ",e)

                if '5' in forms_to_download or back_up_data:
                    # --- 5. Faculty Awards & Achievement ---
                    sheet5 = workbook.create_sheet("5. Faculty Awards & Achievement")
                    headers_5 = ['Timestamp', 'Email address', 'Session', 'Faculty Name', 'Employee ID',
                                   'Designation', 'Department', 'Name of the Award/Achievement', 'Category','Position / Award For',
                                   'Agency/Organization', 'Prize', 'Date of Award', 'Remark',
                                   'All information filled by me is correct and I will submit proof and other related document whenever is asked']
                    if user_type == 'ad' or user_type == 'spa':
                        headers_5.insert(12,'Upload Award Certificate/Proof')
                    sheet5.append(headers_5)

                    # for making text bold
                    for cell in sheet5[1]:
                        cell.font = Font(name='Arial', size=11, bold=True)

                    file_path_links = []
                    for item in awards_and_achievments.objects.filter(query):
                        row_data = [timezone.localtime(item.created_at).strftime("%d-%m-%Y %H:%M:%S"), item.email.email, item.get_session_display(),
                                       item.email.name, item.email.emp_id, item.email.get_designation_display(), item.email.get_department_display(),
                                       item.noaa, item.get_category_display(), item.paf,
                                       item.ao, item.prize,
                                       item.remark, "I AGREE"]
                        if item.proof_file and (user_type == 'ad' or user_type == 'spa'):
                            proof_file = "https://uttkarsh007.pythonanywhere.com" + item.proof_file.url
                            row_data.insert(12,proof_file)
                            file_path_links.append(item.proof_file.path)
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

                    for file_path in file_path_links:
                        try:
                            zip_ref.write(file_path, arcname=f"Faculty Awards & Achievement Files/{os.path.basename(file_path)}")
                        except Exception as e:
                            print("File not Found: ",e)

                if '6' in forms_to_download or back_up_data:
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

                    file_path_links = []
                    for item in sponsored_research.objects.filter(query):
                        row_data = [timezone.localtime(item.created_at).strftime("%d-%m-%Y %H:%M:%S"), item.email.email, item.email.name,
                                       item.email.emp_id, item.email.get_department_display(), item.get_category_display(),
                                       item.nofa, item.dop,
                                       item.amount, item.get_session_display(), item.get_status_display(),
                                       ]
                        if item.proof_file and (user_type == 'ad' or user_type == 'spa'):
                            proof_file = "https://uttkarsh007.pythonanywhere.com" + item.proof_file.url
                            row_data.append(proof_file)
                            file_path_links.append(item.proof_file.path)
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

                    for file_path in file_path_links:
                        try:
                            zip_ref.write(file_path, arcname=f"Sponsored Research／Grant Received／Consultancy Files/{os.path.basename(file_path)}")
                        except Exception as e:
                            print("File not Found: ",e)

                if '7_1' in forms_to_download or back_up_data:
                    # --- 7.1 Research Publication - Journal ---
                    sheet7 = workbook.create_sheet("7.1Research Publication-Journal")
                    headers_7 = ['Timestamp', 'Email address', 'Employee ID', 'Name of the author(s)', 'Department',
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

                    file_path_links = []
                    for item in research_journal.objects.filter(query):
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
                            file_path_links.append(item.proof_file.path)
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

                    for file_path in file_path_links:
                        try:
                            zip_ref.write(file_path, arcname=f"Research Publication - Journal Files/{os.path.basename(file_path)}")
                        except Exception as e:
                            print("File not Found: ",e)

                if '7_2' in forms_to_download or back_up_data:
                    # --- 7.2 Conference Publication ---
                    sheet8 = workbook.create_sheet("7.2 Conference Publication")
                    headers_8 = ['Timestamp', 'Email address', 'Department', 'Employee ID', 'Name of author',
                                   'Title of the Conference', 'Title of paper', 'Title of the proceedings of the conference','Level(National/International)', 'ISBN/ISSN number of the proceeding','Name of the Publisher', 'Published Date', 'Session',
                                   'DOI', 'Web Link', 'Affiliating Institute at the time of publication', 'Indexed by', 'Is SKIT student associated?', 'If Yes , Write student(s) details (Program, Branch, RollNo/EnrollNo, Name)']
                    if user_type == 'ad' or user_type == 'spa':
                        headers_8.append('Upload Full Paper')
                    sheet8.append(headers_8)

                    # for making text bold
                    for cell in sheet8[1]:
                        cell.font = Font(name='Arial', size=11, bold=True)

                    file_path_links = []
                    for item in research_conference.objects.filter(query):
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
                            file_path_links.append(item.proof_file.path)
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

                    for file_path in file_path_links:
                        try:
                            zip_ref.write(file_path, arcname=f"Research Publication - Conference Publication Files/{os.path.basename(file_path)}")
                        except Exception as e:
                            print("File not Found: ",e)

                if '7_3' in forms_to_download or back_up_data:
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

                    file_path_links = []
                    for item in research_book.objects.filter(query):
                        row_data = [timezone.localtime(item.created_at).strftime("%d-%m-%Y %H:%M:%S"), item.email.email, item.email.get_department_display(), item.email.emp_id,
                                       item.noa, item.tob,
                                       item.top, item.get_level_display(), item.isbn,
                                       item.nop, item.pd, item.get_session_display(),
                                       item.doi, item.lwj,
                                       item.aitp, item.index_by, item.get_ssa_display(), item.details]
                        if item.proof_file and (user_type == 'ad' or user_type == 'spa'):
                            proof_file = "https://uttkarsh007.pythonanywhere.com" + item.proof_file.url
                            row_data.append(proof_file)
                            file_path_links.append(item.proof_file.path)
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

                    for file_path in file_path_links:
                        try:
                            zip_ref.write(file_path, arcname=f"Research Publication - Book and Book Chapters Files/{os.path.basename(file_path)}")
                        except Exception as e:
                            print("File not Found: ",e)

                if '7_4' in forms_to_download or back_up_data:
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

                    file_path_links = []
                    for item in patents.objects.filter(query):
                        row_data = [timezone.localtime(item.created_at).strftime("%d-%m-%Y %H:%M:%S"), item.email.email, item.get_session_display(), item.email.get_department_display(), item.email.emp_id,
                                       item.email.name, item.get_sop_display(),
                                       item.ag, item.gi, item.get_pg_display(),
                                       item.top, item.gc, item.pfd,
                                       item.pd.strftime("%d-%m-%Y"), item.get_ssa_display(), item.details,
                                       item.link]
                        if item.proof_file and (user_type == 'ad' or user_type == 'spa'):
                            proof_file = "https://uttkarsh007.pythonanywhere.com" + item.proof_file.url
                            row_data.append(proof_file)
                            file_path_links.append(item.proof_file.path)
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

                    for file_path in file_path_links:
                        try:
                            zip_ref.write(file_path, arcname=f"Patents Files/{os.path.basename(file_path)}")
                        except Exception as e:
                            print("File not Found: ",e)

                if '8' in forms_to_download or back_up_data:
                    # --- 8. M.TechPh.D Guided ---
                    sheet11 = workbook.create_sheet("8. M.Tech,Ph.D Guided")
                    sheet11.append(['Timestamp', 'Email address','Session', 'Faculty Name', 'Employee ID', 'Department',
                                   'Name of the student Guided', 'Program of Student', 'Enrollment Number of Student',
                                   'University Roll Number of Student', 'Enrollment Year of Student', 'Title of the Dissertation', 'Supervisor / Co-supervisor', 'Date of Viva-Voce',
                                   'Name of external examiner'])

                    # for making text bold
                    for cell in sheet11[1]:
                        cell.font = Font(bold=True)

                    for item in guided.objects.filter(query):
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

                    for file_path in file_path_links:
                        try:
                            zip_ref.write(file_path, arcname=f"M.Tech／Ph.D Guided Files/{os.path.basename(file_path)}")
                        except Exception as e:
                            print("File not Found: ",e)

                if '9' in forms_to_download or back_up_data:
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

                    file_path_links = []
                    for item in resource.objects.filter(query):
                        row_data = [timezone.localtime(item.created_at).strftime("%d-%m-%Y %H:%M:%S"), item.email.email, item.get_session_display(), item.email.name, item.email.emp_id,
                                       item.email.get_department_display(), item.get_category_display(),
                                       item.toe, item.sa, item.get_rpt_display(),
                                       item.doe, item.begi_date.strftime("%d-%m-%Y"), item.end_date.strftime("%d-%m-%Y"),
                                       item.venue]
                        if item.proof_file and (user_type == 'ad' or user_type == 'spa'):
                            proof_file = "https://uttkarsh007.pythonanywhere.com" + item.proof_file.url
                            row_data.append(proof_file)
                            file_path_links.append(item.proof_file.path)
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

                    for file_path in file_path_links:
                        try:
                            zip_ref.write(file_path, arcname=f"Resource Person Files/{os.path.basename(file_path)}")
                        except Exception as e:
                            print("File not Found: ",e)

                with zip_ref.open("Faculty Data Collection Response Sheet.xlsx", "w") as excel_file:
                    workbook.save(excel_file)

            response.write(zip_buffer.getvalue())
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