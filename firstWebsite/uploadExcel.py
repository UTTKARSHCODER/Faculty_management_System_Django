import pandas as pd
from django.shortcuts import redirect, render
from tablib import Dataset
from django.contrib import messages
from django.urls import reverse

from firstWebsite.modals import Student_Directory, Faculty


def upload_excel(request, pk):
    if pk:
        if request.method == 'POST':
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
            if pk == 0:
                df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
                for data in imported_data.dict:
                    value = Student_Directory(name=data['name'],roll_no=data['roll_no'],college_id=data['college_id'],email=data['email'],student_phone_no=data['student_phone_no'],parent_phone_no=data['parent_phone_no'],address=data['address'])
                    value.save()

                messages.success(request,'We are glad to share that your excel file is uploaded successfully!')
                return redirect(reverse('student-directory'))

            elif pk == 1:
                df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
                for data in df.to_dict(orient='records'):
                    if not data['name']:
                        continue

                    value = Faculty(name=data['name'],emp_id=data['employee_id'],email=data['email'],department=data['department'],contact_number=data['contact_number'],status="NR")
                    value.save()

                return redirect(reverse('directory'))
            else:
                return render(request, '404.html')
    return render(request,'404.html')