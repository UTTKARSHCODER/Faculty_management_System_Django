import pandas as pd
from django.shortcuts import redirect, render
from tablib import Dataset
from django.contrib import messages
from django.urls import reverse
from django.http import JsonResponse
import re

from firstWebsite.modals import Student_Directory, Faculty, accept, Faculty_participation_data, level, mode, category, \
    session, mooc_course, doc, medals, pertopper, eof_choices, sponsors, events, department, awards_and_achievments


def new_user_registration(data, username):
    dept_db_val = {choice.label: choice.value for choice in department}

    try:
        user_instance = Faculty.objects.get(email=data['email_address'])
    except Faculty.DoesNotExist:
        data['department'] = re.sub(r' (\()', r'\1', data['department'])
        user_instance = Faculty(name=data[username], emp_id=data['employee_id'],
                                email=data['email_address'],
                                department=dept_db_val.get(data['department'], "CSE"),
                                contact_number="9874563210", status="NR")
        user_instance.save()

    return user_instance


def upload_excel(request, pk):
    if pk and request.method == 'POST':

        dataset = Dataset()
        new_data = request.FILES['excel_file']
        if not new_data or new_data.name == '':
            messages.error(request,'No file is selected or invalid file')
            return "No file selected or invalid file", 400
        imported_data = dataset.load(new_data.read(), format='xlsx')
        df = pd.DataFrame(
            imported_data.dict,
            columns=imported_data.headers
        )
        df.columns = (
            df.columns
            .str.strip()
            .str.lower()
            .str.replace(r'[\s&./()]', '_', regex=True)
            .str.replace(r'_+', '_', regex=True)
            .str.strip('_')
        )

        category_db_val = {choice.label: choice.value for choice in category}
        session_db_val = {choice.label: choice.value for choice in session}
        approval_db_val = {choice.label: choice.value for choice in accept}

        if pk == 0:
            for data in imported_data.dict:
                value = Student_Directory(name=data['name'],roll_no=data['roll_no'],college_id=data['college_id'],email=data['email'],student_phone_no=data['student_phone_no'],parent_phone_no=data['parent_phone_no'],address=data['address'])
                value.save()

            messages.success(request,'We are glad to share that your excel file is uploaded successfully!')
            return redirect(reverse('student-directory'))

        elif pk == 14:
            for data in df.to_dict(orient='records'):
                if not data['name']:
                    continue

                value = new_user_registration(data, 'name')
                value.save()

            return redirect(reverse('manage_access'))

        elif pk == 1:

            level_db_val = {choice.label: choice.value for choice in level}
            mode_db_val = {choice.label: choice.value for choice in mode}
            for data in df.to_dict(orient='records'):
                if not data['title_of_the_program']:
                    continue
                try:
                    data['grant_received_from_skit_yes_no'] = approval_db_val.get(data['grant_received_from_skit_yes_no'],"N")
                    data['proof_enclosed_yes_no'] = approval_db_val.get(data['proof_enclosed_yes_no'],"N")
                    data['level'] = level_db_val.get(data['level'],"Na")
                    data['mode_offline_online'] = mode_db_val.get(data['mode_offline_online'],"Of")
                    data['conference_fdp_workshop_seminar_sttp'] = category_db_val.get(data['conference_fdp_workshop_seminar_sttp'],"OTH")
                    data['session'] = session_db_val.get(data['session'],"2024-25")


                    user_instance = new_user_registration(data, 'name_of_faculty_memeber')

                    value = Faculty_participation_data(category=data['conference_fdp_workshop_seminar_sttp'],top=data['title_of_the_program'],mode=data['mode_offline_online'],
                                                       level=data['level'],organizer=data['organizer'],sponsors=data['sponsored_by'],
                                                       approval=data['grant_received_from_skit_yes_no'],begi_date=data['from_date'],end_date=data['to_date'],
                                                       session=data['session'],no_of_days=data['no_of_days'],proof_enclosed=data['proof_enclosed_yes_no'],
                                                       proof_file=data['upload_certificate_proof'],email=user_instance)
                    value.save()
                except KeyError as e:
                    messages.error(request, f'Your Excel file does not have column {e}')

        elif pk == 2:

            for data in df.to_dict(orient='records'):

                doc_db_val = {choice.label: choice.value for choice in doc}
                ctype_db_val = {choice.label: choice.value for choice in medals}
                topper_db_val = {choice.label: choice.value for choice in pertopper}

                try:

                    if not data['name_of_the_course']:
                        continue

                    data['duration_of_course'] = doc_db_val.get(data['duration_of_course'], "O")
                    data['certificate_type'] = ctype_db_val.get(data['certificate_type'], "SC")
                    data['any_category_from_below'] = topper_db_val.get(data['any_category_from_below'], "NA")
                    data['type_of_course'] = category_db_val.get(data['type_of_course'], "OTH")
                    data['session'] = session_db_val.get(data['session'], "2024-25")

                    user_instance = new_user_registration(data, 'name_of_faculty_memeber')

                    value = mooc_course(category=data['type_of_course'], timeline=data['timeline_of_course'],
                                        noc=data['name_of_the_course'],
                                        doc=data['duration_of_course'], begi_date=data['start_date_of_course'],
                                        end_date=data['end_date_of_course'],
                                        offer=data['offering_agency_organizer'], ctype=data['certificate_type'],
                                        topper_in=data['any_category_from_below'],
                                        session=data['session'], remarks=data['remark_if_any'],
                                        proof_file=data['upload_certificate'], email=user_instance)
                    value.save()

                except KeyError as e:
                    messages.error(request,f'Your Excel file does not have column {e}')


        elif pk == 3:

            for data in df.to_dict(orient='records'):

                eof_db_val = {choice.label: choice.value for choice in eof_choices}
                ct_db_val = {choice.label: choice.value for choice in sponsors}
                # Number of staff member participated
                # (Provide list of staff members with  their EMPLOYEE ID & Certificates)
                json_list = []

                try:
                    if not data['name_of_faculty_coordinator_s']:
                        continue

                    for values in data['event_organized_for'].split(','):
                        mapped_value = eof_db_val.get(values.strip(), "S")
                        json_list.append(mapped_value)

                    data['event_organized_for'] = json_list
                    data['sponsored_non_sponsored'] = ct_db_val.get(data['sponsored_non_sponsored'], "NS")
                    data['grant_received_yes_no'] = approval_db_val.get(data['grant_received_yes_no'], "N")
                    data['event_report_attached_in_proper_format_yes_no'] = approval_db_val.get(
                        data['event_report_attached_in_proper_format_yes_no'], "N")
                    data['type_of_event'] = category_db_val.get(data['type_of_event'], "OTH")
                    data['session'] = session_db_val.get(data['academic_session'], "2024-25")

                    user_instance = new_user_registration(data, '')

                    value = events(category=data['type_of_event'], eof=data['event_organized_for'],
                                   nofc=data['name_of_faculty_coordinator_s'],
                                   topdpo=data['title_of_the_professional_development_program_organized'],
                                   nop=data['no_of_participants'],
                                   adcc=data['academic_department_cell_committees_labs_coe'],
                                   session=data['academic_session'], ct=data['sponsored_non_sponsored'],
                                   nosa=data['name_of_sponsoring_agency_if_sponsored'],
                                   cd=data['collaboration_details'], begi_date=data['start_date_of_the_event'],
                                   end_date=data['end_date_the_event'], gr=data['grant_received_yes_no'],
                                   gd=data['grant_details'],
                                   awpsfooe=data['association_with_professional_societies_for_organization_of_event'],
                                   nossp=data[
                                       'number_of_skit_students_participated_provide_list_of_students_with_their_rtu_roll_no_certificates'],
                                   nosmp=data[
                                       'number_of_staff_member_participated_provide_list_of_staff_members_with_their_employee_id_certificates'],
                                   eraipf=data['event_report_attached_in_proper_format_yes_no'],
                                   remarks=data['any_other_remark'], proof_file=data['upload_event_report'],
                                   email=user_instance)
                    value.save()

                except KeyError as e:
                    messages.error(request,f'Your Excel file does not have column {e}')

        elif pk == 4:
            for data in df.to_dict(orient='records'):
                try:
                    if not data['name_of_the_award_achievement']:
                        continue

                    data['category'] = category_db_val.get(data['category'], "OTH")
                    data['session'] = session_db_val.get(data['session'], "2024-25")

                    user_instance = new_user_registration(data, 'faculty_name')

                    value = awards_and_achievments(category=data['category'], noaa=data['name_of_the_award_achievement'],
                                   paf=data['position_award_for'],
                                   ao=data['agency_organization'],
                                   prize=data['prize'],
                                   ad=data['date_of_award'],
                                   remark=data['remark'], proof_file=data['upload_award_certificate_proof'],
                                   session=data['session'],
                                   email=user_instance)
                    value.save()

                except KeyError as e:
                    messages.error(request,f'Your Excel file does not have column {e}')

        else:
            return render(request, '404.html')

        messages.success(request, "File uploaded successfully!")
        return JsonResponse({'status': 'success'})

    return render(request,'404.html')