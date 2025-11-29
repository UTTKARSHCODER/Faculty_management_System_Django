from import_export import resources
from .modals import Student_Directory

class StudentResources(resources.ModelResource):
    class meta:
        model = Student_Directory