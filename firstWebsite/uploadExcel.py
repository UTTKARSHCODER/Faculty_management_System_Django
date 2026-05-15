import pandas as pd
from django.shortcuts import redirect, render
from tablib import Dataset
from django.contrib import messages
from django.urls import reverse
from django.http import JsonResponse
import re

from firstWebsite.modals import Faculty, accept, Faculty_participation_data, level, mode, category, \
    session, mooc_course, doc, medals, pertopper, eof_choices, sponsors, events, department, awards_and_achievments, \
    index_by, quartile, research_journal, research_conference, research_book, patents, type_of_patent, status_of_patent, \
    enrollmentYear, survillance, guided, resource_person_type, resource, sponsored_research, status


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


def upload_excel(request, form_no):
    if form_no and request.method == 'POST':

        dataset = Dataset()
        new_data = request.FILES['excel_file']
        if not new_data or new_data.name == '':
            messages.error(request, 'No file is selected or invalid file')
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
            .str.replace(r'[^\w]+', '_', regex=True)
            .str.strip('_')
        )

        category_db_val = {choice.label: choice.value for choice in category}
        session_db_val = {choice.label: choice.value for choice in session}
        approval_db_val = {choice.label: choice.value for choice in accept}

        if form_no == 0:
            for data in imported_data.dict:
                value = Student_Directory(name=data['name'], roll_no=data['roll_no'], college_id=data['college_id'],
                                          email=data['email'], student_phone_no=data['student_phone_no'],
                                          parent_phone_no=data['parent_phone_no'], address=data['address'])
                value.save()

            messages.success(request, 'We are glad to share that your excel file is uploaded successfully!')
            return redirect(reverse('student-directory'))

        elif form_no == 14:
            for data in df.to_dict(orient='records'):
                if not data['name']:
                    continue

                value = new_user_registration(data, 'name')
                value.save()

            return redirect(reverse('manage_access'))

        elif form_no == 1:

            level_db_val = {choice.label: choice.value for choice in level}
            mode_db_val = {choice.label: choice.value for choice in mode}
            for data in df.to_dict(orient='records'):
                if not data['title_of_the_program']:
                    continue
                try:
                    data['grant_received_from_skit_yes_no'] = approval_db_val.get(
                        data['grant_received_from_skit_yes_no'], "N")
                    data['proof_enclosed_yes_no'] = approval_db_val.get(data['proof_enclosed_yes_no'], "N")
                    data['level'] = level_db_val.get(data['level'], "Na")
                    data['mode_offline_online'] = mode_db_val.get(data['mode_offline_online'], "Of")
                    data['conference_fdp_workshop_seminar_sttp'] = category_db_val.get(
                        data['conference_fdp_workshop_seminar_sttp'], "OTH")
                    data['session'] = session_db_val.get(data['session'], "2024-25")

                    user_instance = new_user_registration(data, 'name_of_faculty_memeber')

                    value = Faculty_participation_data(category=data['conference_fdp_workshop_seminar_sttp'],
                                                       top=data['title_of_the_program'],
                                                       mode=data['mode_offline_online'],
                                                       level=data['level'], organizer=data['organizer'],
                                                       sponsors=data['sponsored_by'],
                                                       approval=data['grant_received_from_skit_yes_no'],
                                                       begi_date=data['from_date'], end_date=data['to_date'],
                                                       session=data['session'], no_of_days=data['no_of_days'],
                                                       proof_enclosed=data['proof_enclosed_yes_no'],
                                                       proof_file=data['upload_certificate_proof'], email=user_instance)
                    value.save()

                except KeyError as e:
                    return JsonResponse({'status': 'failed', 'error': f'Your Excel does not contain column {e}'})

                except Exception:
                    return JsonResponse({'status': 'failed', 'error': 'Internal Server Error occured while saving!'})

        elif form_no == 2:

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
                    return JsonResponse({'status': 'failed', 'error': f'Your Excel does not contain column {e}'})

                except Exception:
                    return JsonResponse({'status': 'failed', 'error': 'Internal Server Error occured while saving!'})


        elif form_no == 3:

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
                    return JsonResponse({'status': 'failed', 'error': f'Your Excel does not contain column {e}'})

                except Exception:
                    return JsonResponse({'status': 'failed', 'error': 'Internal Server Error occured while saving!'})

        elif form_no == 4:
            for data in df.to_dict(orient='records'):
                try:
                    if not data['name_of_the_award_achievement']:
                        continue

                    data['category'] = category_db_val.get(data['category'], "OTH")
                    data['session'] = session_db_val.get(data['session'], "2024-25")

                    user_instance = new_user_registration(data, 'faculty_name')

                    value = awards_and_achievments(category=data['category'],
                                                   noaa=data['name_of_the_award_achievement'],
                                                   paf=data['position_award_for'],
                                                   ao=data['agency_organization'],
                                                   prize=data['prize'],
                                                   ad=data['date_of_award'],
                                                   remark=data['remark'],
                                                   proof_file=data['upload_award_certificate_proof'],
                                                   session=data['session'],
                                                   email=user_instance)
                    value.save()

                except KeyError as e:
                    return JsonResponse({'status': 'failed', 'error': f'Your Excel does not contain column {e}'})

                except Exception:
                    return JsonResponse({'status': 'failed', 'error': 'Internal Server Error occured while saving!'})

        elif form_no == 5:
            for data in df.to_dict(orient='records'):
                status_db_val = {choice.label: choice.value for choice in status}
                try:
                    if not data['name_of_candidate_pi_co_pi']:
                        continue

                    data['category'] = category_db_val.get(data['category'], "OTH")
                    data['session_in_which_grant_research_project_consultancy_received'] = session_db_val.get(data['session_in_which_grant_research_project_consultancy_received'], "2024-25")
                    data['status'] = status_db_val.get(data['status'], "ON")

                    user_instance = new_user_registration(data, 'name_of_candidate_pi_co_pi')

                    value = sponsored_research(category=data['category'],
                                                   nofa=data['name_of_the_funding_agency_msme_dst_csir_serb_industry_etc'],
                                                   dop=data['duration_of_project_in_years'],
                                                   amount=data['amount_in_rs'],
                                                   session=data['session_in_which_grant_research_project_consultancy_received'],
                                                   status=data['status'],
                                                   proof_file=data['upload_proof'],
                                                   email=user_instance)
                    value.save()

                except KeyError as e:
                    return JsonResponse({'status': 'failed', 'error': f'Your Excel does not contain column {e}'})

                except Exception:
                    return JsonResponse({'status': 'failed', 'error': 'Internal Server Error occured while saving!'})

        elif form_no == 6:
            for data in df.to_dict(orient='records'):
                level_db_val = {choice.label: choice.value for choice in level}
                index_by_db_val = {choice.label: choice.value for choice in index_by}
                quartile_db_val = {choice.label: choice.value for choice in quartile}

                try:
                    if not data['name_of_the_author_s']:
                        continue

                    data['level_national_international'] = level_db_val.get(data['level_national_international'], "In")
                    data['is_skit_student_associated'] = approval_db_val.get(data['is_skit_student_associated'], "N")
                    data['indexed_by'] = index_by_db_val.get(data['indexed_by'], "O")
                    data['quartile'] = quartile_db_val.get(data['quartile'], "NA")
                    data['session'] = session_db_val.get(data['session'], "2024-25")

                    user_instance = new_user_registration(data, '')

                    value = research_journal(noa=data['name_of_the_author_s'], top=data['title_of_paper'],
                                                   noj=data['name_of_journal'],
                                                   nop=data['name_of_the_publisher'],
                                                   vi=data['volume_issue'],
                                                   pn=data['page_no'],
                                                   pd=data['published_date'], session=data['session'],
                                                   isnp=data['issn_number_print'], isno=data['issn_number_online'], level=data['level_national_international'],
                                                   doi=data['doi'], lwj=data['link_to_website_of_the_journal'], lap=data['link_to_article_paper_abstract_of_the_article_direct_link_to_the_webpage_where_the_abstract_of_paper_is_displayed'],
                                                   lrsj=data['link_to_the_recognition_in_scopus_enlistment_of_the_journal'], aiop=data['affiliating_institute_at_the_time_of_publication'], ssa=data['is_skit_student_associated'],
                                                   details=data['if_yes_write_student_s_details_program_branch_rollno_enrollno_name'], index_by=data['indexed_by'],
                                                   quartile=data['quartile'], proof_file=data['upload_full_paper'],
                                                   email=user_instance)
                    value.save()


                except KeyError as e:
                    return JsonResponse({'status': 'failed', 'error': f'Your Excel does not contain column {e}'})

                except Exception:
                    return JsonResponse({'status': 'failed', 'error': 'Internal Server Error occured while saving!'})

        elif form_no == 7:
            for data in df.to_dict(orient='records'):
                level_db_val = {choice.label: choice.value for choice in level}

                try:
                    if not data['name_of_the_author_s']:
                        continue

                    data['level_national_international'] = level_db_val.get(data['level_national_international'], "In")
                    data['is_skit_student_associated'] = approval_db_val.get(data['is_skit_student_associated'], "N")
                    data['session'] = session_db_val.get(data['session'], "2024-25")

                    user_instance = new_user_registration(data, '')

                    value = research_conference(noa=data['name_of_the_author_s'], toc=data['title_of_the_conference'],
                                                   top=data['title_of_paper'],
                                                   topc=data['title_of_the_proceedings_of_the_conference'],
                                                   level=data['level_national_international'],
                                                   isnp=data['isbn_issn_number_of_the_proceeding'],
                                                   nop=data['name_of_the_publisher'], pd=data['published_date'],
                                                   session=data['session'], doi=data['doi'], lwj=data['web_link'],
                                                   aitp=data['affiliating_institute_at_the_time_of_publication'], ssa=data['is_skit_student_associated'],
                                                   details=data['if_yes_write_student_s_details_program_branch_rollno_enrollno_name'], index_by=data['indexed_by'],
                                                   proof_file=data['upload_full_paper'],
                                                   email=user_instance)
                    value.save()


                except KeyError as e:
                    return JsonResponse({'status': 'failed', 'error': f'Your Excel does not contain column {e}'})

                except Exception:
                    return JsonResponse({'status': 'failed', 'error': 'Internal Server Error occured while saving!'})

        elif form_no == 8:
            for data in df.to_dict(orient='records'):
                level_db_val = {choice.label: choice.value for choice in level}

                try:
                    if not data['name_of_the_author_editor']:
                        continue

                    data['level_national_international'] = level_db_val.get(data['level_national_international'], "In")
                    data['is_skit_student_associated'] = approval_db_val.get(data['is_skit_student_associated'], "N")
                    data['session'] = session_db_val.get(data['session'], "2024-25")

                    user_instance = new_user_registration(data, '')

                    value = research_book(noa=data['name_of_the_author_editor'], tob=data['title_of_the_book'],
                                                   top=data['title_of_the_chapter_published'],
                                                   level=data['level_national_international'],
                                                   isbn=data['isbn'],
                                                   nop=data['name_of_the_publisher'], pd=data['published_date'],
                                                   session=data['session'], doi=data['doi'], lwj=data['web_link'],
                                                   aitp=data['affiliating_institute_at_the_time_of_publication'], ssa=data['is_skit_student_associated'],
                                                   details=data['if_yes_write_student_s_details_program_branch_rollno_enrollno_name'], index_by=data['indexed_by'],
                                                   proof_file=data['upload_proof_book_chapter_front_page_document_etc'],
                                                   email=user_instance)
                    value.save()


                except KeyError as e:
                    return JsonResponse({'status': 'failed', 'error': f'Your Excel does not contain column {e}'})

                except Exception:
                    return JsonResponse({'status': 'failed', 'error': 'Internal Server Error occured while saving!'})

        elif form_no == 9:
            for data in df.to_dict(orient='records'):
                type_of_patent_db_val = {choice.label: choice.value for choice in type_of_patent}
                status_of_patent_db_val = {choice.label: choice.value for choice in status_of_patent}

                try:
                    if not data['name_of_faculty']:
                        continue

                    data['status_of_patent'] = status_of_patent_db_val.get(data['status_of_patent'], "P")
                    data['type_of_patent'] = type_of_patent_db_val.get(data['type_of_patent'], "I")
                    data['is_skit_student_associated'] = approval_db_val.get(data['is_skit_student_associated'], "N")
                    data['session'] = session_db_val.get(data['session'], "2024-25")

                    user_instance = new_user_registration(data, 'name_of_faculty')

                    value = patents(sop=data['status_of_patent'], gi=data['granted_id'],
                                                   ag=data['application_id'],
                                                   top=data['title_of_patent'],
                                                   gc=data['granted_country'],
                                                   pfd=data['patent_filed_date'], pd=data['publication_date'],
                                                   session=data['session'], pg=data['type_of_patent'], ssa=data['is_skit_student_associated'],
                                                   details=data['if_yes_write_student_s_details_program_branch_rollno_enrollno_name'], link=data['link'],
                                                   proof_file=data['upload_proof'],
                                                   email=user_instance)
                    value.save()


                except KeyError as e:
                    return JsonResponse({'status': 'failed', 'error': f'Your Excel does not contain column {e}'})

                except Exception:
                    return JsonResponse({'status': 'failed', 'error': 'Internal Server Error occured while saving!'})

        elif form_no == 10:
            for data in df.to_dict(orient='records'):
                visor_db_val = {choice.label: choice.value for choice in survillance}
                enrollment_year_db_val = {choice.label: choice.value for choice in enrollmentYear}

                try:
                    if not data['faculty_name']:
                        continue

                    data['program_of_student'] = category_db_val.get(data['program_of_student'], "OTH")
                    data['enrollment_year_of_student'] = enrollment_year_db_val.get(data['enrollment_year_of_student'], "2023")
                    data['supervisor_co_supervisor'] = visor_db_val.get(data['supervisor_co_supervisor'], "S")
                    data['session'] = session_db_val.get(data['session'], "2024-25")

                    user_instance = new_user_registration(data, 'faculty_name')

                    value = guided(category=data['program_of_student'], nos=data['name_of_the_student_guided'],
                                                   ens=data['enrollment_number_of_student'],
                                                   urns=data['university_roll_number_of_student'],
                                                   eys=data['enrollment_year_of_student'],
                                                   tod=data['title_of_the_dissertation'], visor=data['supervisor_co_supervisor'],
                                                   dov=data['date_of_viva_voce'], noe=data['name_of_external_examiner'], session=data['session'],
                                                   email=user_instance)
                    value.save()



                except KeyError as e:
                    return JsonResponse({'status': 'failed', 'error': f'Your Excel does not contain column {e}'})

                except Exception:
                    return JsonResponse({'status': 'failed', 'error': 'Internal Server Error occured while saving!'})

        elif form_no == 11:
            for data in df.to_dict(orient='records'):
                resource_person_type_db_val = {choice.label: choice.value for choice in resource_person_type}

                try:
                    if not data['name_of_faculty_member']:
                        continue

                    data['resource_person_in'] = category_db_val.get(data['resource_person_in'], "OTH")
                    data['resource_person_type'] = resource_person_type_db_val.get(data['resource_person_type'],"O")
                    data['session'] = session_db_val.get(data['session'], "2024-25")

                    user_instance = new_user_registration(data, 'name_of_faculty_member')

                    value = resource(category=data['resource_person_in'], toe=data['title_of_event_exam_name'],
                                   sa=data['subject_area_subject_name_lab_name_session_name'],
                                   doe=data['duration_of_event_in_days'],
                                   rpt=data['resource_person_type'],
                                   begi_date=data['date_from'], end_date=data['date_to'],
                                   session=data['session'], venue=data['venue'],
                                   proof_file=data['proof_certificate_mail'],
                                   email=user_instance)
                    value.save()


                except KeyError as e:
                    return JsonResponse({'status': 'failed', 'error': f'Your Excel does not contain column {e}'})

                except Exception:
                    return JsonResponse({'status': 'failed', 'error': 'Internal Server Error occured while saving!'})

        else:
            return render(request, '404.html')

        messages.success(request, "File uploaded successfully!")
        return JsonResponse({'status': 'success'})

    return render(request, '404.html')
