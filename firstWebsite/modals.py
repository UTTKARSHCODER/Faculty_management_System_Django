import datetime
import os
import uuid

from django.db import models
from django.db.models import CASCADE
from django.utils.dateparse import parse_date
from multiselectfield import MultiSelectField
from django.utils import timezone
import jwt
from MyFirstDjangoWebsite import settings

class batch(models.TextChoices):
    CS_A = "3CS-A",
    CS_B = "3CS-B",
    CS_C = "3CS-C",
    CS_D = "3CS-D",
    CS_E = "3CS-E",
    CS_F = "3CS-F",
    CS_AI_A = "3CS(AI)-A",
    CS_AI_B = "3CS(AI)-B",
    CS_DS_A = "3CS(DS)-A",
    CS_IOT_A = "3CS(IOT)-A",
    CS_IOT_B = "3CS(IOT)-B"

class sponsors(models.TextChoices):
    SPONSORED = "S", "Sponsored",
    NON_SPONSORED = "NS", "Non-Sponsored"

def generate_session_choices():
  """Generates a list of academic sessions dynamically,

  ranging from 2 years in the past to 5 years into the future.
  """
  current_date = timezone.now()
  current_year = current_date.year

  # If we are before July, the current academic session started last year
  if current_date.month < 7:
      base_year = current_year - 1
  else:
      base_year = current_year

  choices = []
  # Adjust the range as needed (e.g., past 2 years to future 5 years)
  for year in range(base_year - 2, base_year + 6):
    next_year_short = str(year + 1)[-2:]
    session_str = f"{year}-{next_year_short}"
    choices.append((session_str, session_str))
  return choices


def get_current_session():
  """Returns the default session string for the current year (e.g., '2026-27')."""
  current_date = timezone.now()
  current_year = current_date.year

  # If it's Jan-June, we are still in the session that started last year
  if current_date.month < 7:
      start_year = current_year - 1
  else:
      start_year = current_year
  next_year_short = str(start_year + 1)[-2:]
  return f"{start_year}-{next_year_short}"

class Role(models.TextChoices):
    FACULTY = "FA", "Faculty",
    ADMIN = "AD", "Admin",
    SUPERADMIN = "SPA", "Superadmin"

class Status(models.TextChoices):
    REGISTERED = "R", "Registered",
    NOTREGISTERED = "NR", "NotRegistered"

class department(models.TextChoices):
    CSE = "CSE","Computer Science & Engineering",
    CSE_AI = "CSE(AI)", "Computer Science & Engineering(AI)",
    CSE_DS = "CSE(DS)", "Computer Science & Engineering(DS)",
    CSE_IOT = "CSE(IOT)", "Computer Science & Engineering(IOT)"

class designation(models.TextChoices):
    ASSISTANT_PROFESSOR_1 = "AP1", "Assistant Professor 1",
    ASSISTANT_PROFESSOR_2 = "AP2", "Assistant Professor 2",
    ASSOCIATE_PROFESSOR_1 = "ASP1", "Associate Professor 1",
    ASSOCIATE_PROFESSOR_2 = "ASP2", "Associate Professor 2",
    PROFESSOR = "P", "Professor"

class area_of_spe(models.TextChoices):
    ARTIFICIAL_INETELLIGENCE_MACHINE_LEARNING = "AIML", "Artificial Intelligence & Machine Learning",
    DATA_INORMATION_SYSTEMS = "DIS", "Data & Information Systems",
    CYBERSECURITY_NETWORKS = "CN", "Cybersecurity & Networks",
    SOFTWARE_SYSTEMS_DEVELOPMENT = "SSD", "Software Systems & Development",
    COMPUTER_SYSTEM_ARCHITECTURE = "CSA", "Computer Systems & Architecture",
    MATHEMATICS = "M", "Mathematics",
    THEORETICAL_COMPUTER_SCIENCE = "TCS", "Theoretical Computer Science",
    OTHER = "O", "Other"

class highest_qual(models.TextChoices):
    BE_BTECH = "BT", "B.E. / B.Tech",
    ME_MTECH = "MT", "M.E. / M.Tech",
    MS = "MS", "M.S.",
    MBA = "MBA", "MBA",
    PHD = "PHD", "Ph.D.",
    POST_DOCTORAL = "PD", "Post-Doctoral Research (Post-Doc)",
    OTHER = "O", "Other"

class gender(models.TextChoices):
    MALE = 'M', "Male",
    FEMALE = 'F', "Female",
    OTHER  = 'O', "Other"

class forms(models.TextChoices):
    FORM_1_1 = "1_1", "Faculty Profile Details",
    FORM_1_2 = "1_2", "Non-teaching Staff Profile Details",
    FORM_2 = "2", "Faculty Participation",
    FORM_3 = "3", "MOOC's/Short Term Course/Course Completion",
    FORM_4 = "4", "Events Organized by Department",
    FORM_5 = "5", "Faculty Awards and Achievements",
    FORM_6 = "6", "Sponsored Research/Grant Received/Consultancy",
    FORM_7_1 = "7_1", "Research Publication - Journals",
    FORM_7_2 = "7_2", "Research Publication - Conference Publication",
    FORM_7_3 = "7_3", "Research Publication - Book and Book Chapters",
    FORM_7_4 = "7_4", "Patents",
    FORM_8 = "8", "M.Tech/Ph.D Guided",
    FORM_9 = "9", "Resource Person",
    NO_FORM = "0", "No Form"

class Faculty(models.Model):
    session_version = models.UUIDField(default=uuid.uuid4, editable=False)
    session = models.CharField(
        max_length=7,
        choices=generate_session_choices,
        default=get_current_session
    )
    form_alloted = MultiSelectField(
        max_length=40,
        choices=forms.choices,
        default=forms.NO_FORM
    )

    @property
    def secure_token(self):
        return jwt.encode(
            {"user_pk": self.pk},
            settings.SECRET_KEY,
            algorithm="HS256"
        )

    @property
    def form_alloted_display_list(self):
        # Grabs the choices dictionary from the field
        choices_dict = dict(forms.choices)

        # Returns a clean Python list of the human-readable names
        return [str(choices_dict.get(choice, choice)) for choice in self.form_alloted]
    name = models.CharField(max_length=255)
    contact_number = models.CharField(max_length=10)
    email = models.EmailField(max_length=254,unique=True)
    department = models.CharField(
        max_length=8,
        choices=department.choices
    )
    gender = models.CharField(
        max_length=1,
        choices=gender.choices,
        default=gender.MALE
    )
    address = models.CharField(max_length=255,default='Address')
    emp_id = models.IntegerField()
    role = models.CharField(
        max_length=3,
        choices=Role.choices,
        default=Role.FACULTY
    )

    def save(self, *args, **kwargs):
        if self.role == "SPA":
            # Get all keys from MY_CHOICES except the restricted one
            all_except_one = [val for val in forms.values if val != forms.NO_FORM]

            # Force the field to contain these values
            self.form_alloted = all_except_one
        elif self.role == "FA":
            only_one = [forms.NO_FORM]
            self.form_alloted = only_one

        super().save(*args, **kwargs)
    status = models.CharField(
        max_length=2,
        choices=Status.choices,
        default=Status.NOTREGISTERED
    )
    designation = models.CharField(
        max_length=4,
        choices=designation.choices,
        default=designation.ASSISTANT_PROFESSOR_1
    )
    aos = models.CharField(
        max_length=4,
        choices=area_of_spe.choices,
        default=area_of_spe.OTHER
    )
    hq = models.CharField(
        max_length=3,
        choices=highest_qual.choices,
        default=highest_qual.OTHER
    )
    univ_name = models.CharField(max_length=255,default='Unknown')
    pshd = models.IntegerField(default=0)
    pan_no = models.CharField(max_length=10,default='AAAEE875AE')
    google_scholar = models.CharField(max_length=255,default="NULL")
    vidwan_profile = models.CharField(max_length=255,default="NULL")
    personal_website_link = models.CharField(max_length=255,null=True)
    dob = models.DateField(default=datetime.date(1970, 1, 1))
    jd = models.DateField(default=datetime.date(1970, 1, 1))
    pd = models.DateField(null=True,blank=True)
    profile_picture = models.FileField(upload_to='uploads/faculty_documents/profile_picture', default=None, null = True,blank = True)
    jr = models.FileField(upload_to='uploads/faculty_documents/joining_report/', default=None, null = True,blank = True)
    of = models.FileField(upload_to='uploads/faculty_documents/offer_letter/', default=None, null = True,blank = True)
    ss = models.FileField(upload_to='uploads/faculty_documents/salary_slip/', default=None, null = True,blank = True)
    hdc = models.FileField(upload_to='uploads/faculty_documents/higher_degree_certificate/', default=None, null = True,blank = True)
    certificate = models.FileField(upload_to='uploads/faculty_documents/certificate/', default=None, null = True,blank = True)
    phd_univ = models.CharField(max_length=255, null = True, blank = True)
    phd_dor = models.DateField(null=True,blank=True)
    norp = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.email

# class faculty_data(models.Model):
#

class accept(models.TextChoices):
    YES = "y", "Yes",
    NO = "N", "No"

class level(models.TextChoices):
    NATIONAL = "Na", "National",
    INTERNATIONAL = "In", "International"

class mode(models.TextChoices):
    ONLINE = "On", "Online",
    OFFLINE = "Of", "Offline"

class category(models.TextChoices):
    FDP = "FDP", "FDP",
    WORKSHOP = "WKP", "Workshop",
    CONFERENCE = "CON", "Conference",
    STTP = "STTP", "Sttp",
    SEMINAR = "SEM", "Seminar",
    WEBINAR = "WEB", "Webinar",
    LECTURE_SERIES = "LS", "Lecture Series",
    SYMPOSIUM = "SYM", "Symposium",
    EXTERNAL_EXAMINATION_UG = "EE(UG)", "External  Examination(UG)",
    EXTERNAL_EXAMINATION_PG = "EE(PG)", "External  Examination(PG)",
    JOURNAL = "JOU","Journal",
    EXPERT_LECTURE = "EL","Expert Lecture",
    EXPERT_TALK = "ET","Expert Talk",
    HACKATHON = "HAT","Hackathon",
    TRAINING = "TRA","Training",
    INTERNSHIP = "INT","Internship",
    BOS = "BOS","BOS",
    DRC = "DRC","DRC",
    SHORT_TERM_COURSES = "STC","Short Term Course",
    MOOC = "MOOC","MOOC",
    INDUCTION_PROGRAM = "IP","Induction Program",
    EDUCATION = "EDU","Education",
    RESEARCH = "REA","Research",
    SPORTS = "SPO","Sports",
    SPONSORED_GRANT= "SG","Sponsored Grant",
    RESEARCH_PROJECT = "RP","Research Project",
    CONSULTANCY = "CONS","Consultancy",
    M_TECH = "M_TECH","M.Tech",
    PHD = "PH_D","Ph.D",
    OTHER = "OTH", "Other"

    @classmethod
    def get_fullvalue(cls, label):
        if not hasattr(cls, '_label_to_value_map'):
            cls._label_to_value_map = {choice.value: choice.label for choice in cls}

        return cls._label_to_value_map.get(label)

def rename_fpd_file(instance, old_filename):
    extension = os.path.splitext(old_filename)[1].lower()
    username = "".join(map(str.capitalize, instance.email.name.split()))
    type_of_event = "_".join(category.get_fullvalue(instance.category).split())
    title_of_program = "_".join(instance.top.split())
    count = Faculty_participation_data.objects.filter(category=instance.category,email=instance.email).values('id').count()
    new_filename = f"{instance.session}_{username}_{type_of_event}_{count + 1}_{title_of_program}{extension}"
    return os.path.join('uploads/fdp_certificate/', new_filename)

class Faculty_participation_data(models.Model):
    @property
    def secure_token(self):
        return jwt.encode(
            {"user_pk": self.pk},
            settings.SECRET_KEY,
            algorithm="HS256"
        )
    category = models.CharField(
        max_length=6,
        choices=category.choices,
        default=category.OTHER
    )
    top = models.CharField(max_length=255,default='Unknown')
    mode = models.CharField(
        max_length=2,
        choices=mode.choices
    )
    level = models.CharField(
        max_length=2,
        choices=level.choices
    )
    organizer = models.CharField(max_length=255)
    sponsors = models.CharField(max_length=255)
    approval = models.CharField(
        max_length=1,
        choices=accept.choices
    )
    begi_date = models.DateField()
    end_date = models.DateField()
    session = models.CharField(
        max_length=7,
        choices=generate_session_choices,
        default=get_current_session
    )
    no_of_days = models.IntegerField()
    proof_enclosed = models.CharField(
        max_length=1,
        choices=accept.choices
    )
    proof_file = models.FileField(upload_to=rename_fpd_file)
    email = models.ForeignKey(Faculty,on_delete=CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.get_category_display() + " " + self.top

class doc(models.TextChoices):
    WEEK_4 = "4", "4 Weeks",
    WEEK_8 = "8", "8 Weeks",
    WEEK_12 = "12", "12 Weeks",
    WEEK_O = "O", "Other than these"

class medals(models.TextChoices):
    GOLD = "G", "Gold",
    SILVER = "S", "Silver",
    ELITE = "E", "Elite",
    SUCCESSFULLY_COMPLETED = "SC", "Successfully Completed"

class pertopper(models.TextChoices):
    PER_1 = "1", "1%",
    PER_2 = "2", "2%",
    PER_5 = "5", "5%",
    PER_10 = "10", "10%"
    PER_NA = "NA", "Not Applicable"

def rename_mooc_file(instance, old_filename):
    extension = os.path.splitext(old_filename)[1].lower()
    raw_date = instance.end_date
    if isinstance(raw_date, str):
        date_obj = parse_date(raw_date)
        year = date_obj.year if date_obj else "no_year"
    elif raw_date:
        year = raw_date.year
    else:
        year = "no_year"
    name_of_course = "_".join(instance.noc.split())
    username = "".join(map(str.capitalize, instance.email.name.split()))
    new_filename = f"{name_of_course}_{username}_{year}{extension}"
    return os.path.join('uploads/mooc_certificate/', new_filename)

class mooc_course(models.Model):
    @property
    def secure_token(self):
        return jwt.encode(
            {"user_pk": self.pk},
            settings.SECRET_KEY,
            algorithm="HS256"
        )
    category = models.CharField(
        max_length=6,
        choices=category.choices,
        default=category.MOOC
    )
    timeline = models.CharField(max_length=255)
    noc = models.CharField(max_length=255)
    doc = models.CharField(
        max_length=2,
        choices=doc.choices
    )
    begi_date = models.DateField()
    end_date = models.DateField()
    offer = models.CharField(max_length=255)
    ctype = models.CharField(
        max_length=2,
        choices=medals.choices
    )
    topper_in = models.CharField(
        max_length=2,
        choices=pertopper.choices
    )
    session = models.CharField(
        max_length=7,
        choices=generate_session_choices,
        default=get_current_session
    )
    remarks = models.CharField(max_length=255,null=True)
    email = models.ForeignKey(Faculty, on_delete=CASCADE)
    proof_file = models.FileField(upload_to=rename_mooc_file)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.noc

class eof_choices(models.TextChoices):
    STUDENTS = "S", "Students",
    TEACHING_STAFF = "TS", "Teaching Staff",
    NON_TEACHING_STAFF = "NTS", "Non-Teaching Staff"

class mapped_sdgs(models.TextChoices):
    SDG_1 = "SDG1", "SDG - 1 (No Poverty)",
    SDG_2 = "SDG2", "SDG - 2 (Zero Hunger)",
    SDG_3 = "SDG3", "SDG - 3 (Good Health And Well-Being)",
    SDG_4 = "SDG4", "SDG - 4 (Quality Education)",
    SDG_5 = "SDG5", "SDG - 5 (Gender Equality)",
    SDG_6 = "SDG6", "SDG - 6 (Clean Water And Sanitation)",
    SDG_7 = "SDG7", "SDG - 7 (Affordable And Clean Energy)",
    SDG_8 = "SDG8", "SDG - 8 (Decent Work And Economic Growth)",
    SDG_9 = "SDG9", "SDG - 9 (Industry And Innovation And Infrastructure)",
    SDG_10 = "SDG10", "SDG - 10 (Reduced Inequalities)",
    SDG_11 = "SDG11", "SDG - 11 (Sustainable Cities And Communities)",
    SDG_12 = "SDG12", "SDG - 12 (Responsible Consumption And Production)",
    SDG_13 = "SDG13", "SDG - 13 (Climate Action)",
    SDG_14 = "SDG14", "SDG - 14 (Life Below Water)",
    SDG_15 = "SDG15", "SDG - 15 (Life On Land)",
    SDG_16 = "SDG16", "SDG - 16 (Peace And Justice And Strong Institutions)",
    SDG_17 = "SDG17", "SDG - 17 (Partnerships For The Goals)",

def rename_events_file(instance, old_filename):
    extension = os.path.splitext(old_filename)[1].lower()
    type_of_event = "_".join(category.get_fullvalue(instance.category).split())
    title_of_event = "_".join(instance.topdpo.split())
    new_filename = f"{instance.session}_{type_of_event}_{title_of_event}{extension}"
    return os.path.join('uploads/events/', new_filename)

class events(models.Model):
    @property
    def secure_token(self):
        return jwt.encode(
            {"user_pk": self.pk},
            settings.SECRET_KEY,
            algorithm="HS256"
        )
    category = models.CharField(
        max_length=6,
        choices=category.choices,
        default=category.OTHER
    )
    eof = models.JSONField(default=list, blank=True)
    @property
    def eof_display_list(self):
        data = self.eof

        # If the database accidentally stored a single string instead of a list
        if isinstance(data, str):
            data = [data]

        # If it's empty or None
        if not data:
            return []

        choice_dict = dict(eof_choices.choices)

        # Now 'NTS' stays together as one key
        return [choice_dict.get(key, key) for key in data]

    nofc = models.CharField(max_length=255,default="Unknown")
    topdpo = models.CharField(max_length=255)
    nop = models.IntegerField()
    adcc = models.CharField(max_length=255)
    session = models.CharField(
        max_length=7,
        choices=generate_session_choices,
        default=get_current_session
    )
    ct = models.CharField(
        max_length=2,
        choices=sponsors.choices
    )
    nosa = models.CharField(max_length=255)
    cd = models.CharField(max_length=255)
    begi_date = models.DateField()
    end_date = models.DateField()
    gr = models.CharField(
        max_length=1,
        choices=accept.choices
    )
    gd = models.CharField(max_length=255)
    actual_expenditure = models.IntegerField(default=0)
    awpsfooe = models.CharField(max_length=255)
    nossp = models.CharField(max_length=255)
    nosmp = models.CharField(max_length=255)
    map_sdg = MultiSelectField(
        max_length=80,
        choices=mapped_sdgs.choices,
        default=mapped_sdgs.SDG_17
    )
    @property
    def map_sdg_display_list(self):
        data = self.map_sdg

        # If it's empty or None
        if not data:
            return []

        # If the database accidentally stored a single string instead of a list
        if isinstance(data, str):
            data = [key.strip() for key in data.split(',') if key.strip()]

        choice_dict = dict(mapped_sdgs.choices)

        # Now 'NTS' stays together as one key
        return [choice_dict.get(key, key) for key in data]

    eraipf = models.CharField(
        max_length=1,
        choices=accept.choices
    )
    proof_file = models.FileField(upload_to=rename_events_file)
    remarks = models.CharField(max_length=255, null = True)
    email = models.ForeignKey(Faculty, on_delete=CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.get_category_display() + " " + self.topdpo

def rename_awards_file(instance, old_filename):
    extension = os.path.splitext(old_filename)[1].lower()
    username = "".join(map(str.capitalize, instance.email.name.split()))
    name_of_award = "_".join(instance.noaa.split())
    new_filename = f"{instance.session}_{username}_{name_of_award}{extension}"
    return os.path.join('uploads/awards/', new_filename)

class awards_and_achievments(models.Model):
    @property
    def secure_token(self):
        return jwt.encode(
            {"user_pk": self.pk},
            settings.SECRET_KEY,
            algorithm="HS256"
        )
    category = models.CharField(
        max_length=6,
        choices=category.choices
    )
    noaa = models.CharField(max_length=255)
    paf = models.CharField(max_length=255)
    ao = models.CharField(max_length=255)
    prize = models.CharField(max_length=255)
    ad = models.DateField()
    remark = models.CharField(max_length=255, null = True)
    proof_file = models.FileField(upload_to=rename_awards_file)
    session = models.CharField(
        max_length=7,
        choices=generate_session_choices,
        default=get_current_session
    )
    email = models.ForeignKey(Faculty, on_delete=CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.get_category_display() + " " + self.noaa

class status(models.TextChoices):
    ONGOING = "ON", "Ongoing",
    COMPLETED = "CM", "Completed"

def rename_sponsored_file(instance, old_filename):
    extension = os.path.splitext(old_filename)[1].lower()
    username = "".join(map(str.capitalize, instance.email.name.split()))
    type_of_event = "_".join(category.get_fullvalue(instance.category).split())
    new_filename = f"{instance.session}_{username}_{type_of_event}{extension}"
    return os.path.join('uploads/sponsored_research/', new_filename)

class sponsored_research(models.Model):
    @property
    def secure_token(self):
        return jwt.encode(
            {"user_pk": self.pk},
            settings.SECRET_KEY,
            algorithm="HS256"
        )
    category = models.CharField(
        max_length=6,
        choices=category.choices
    )
    nofa = models.CharField(max_length=255)
    dop = models.IntegerField()
    amount = models.IntegerField()
    session = models.CharField(
        max_length=7,
        choices=generate_session_choices,
        default=get_current_session
    )
    status = models.CharField(
        max_length=2,
        choices=status.choices
    )
    proof_file = models.FileField(upload_to=rename_sponsored_file)
    email = models.ForeignKey(Faculty, on_delete=CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.get_category_display() + " " + self.nofa

class index_by(models.TextChoices):
    SCI = "S", "SCI/SCIE/SSCI",
    SCOPUS = "NS", "Scopus",
    ESCI = "ES", "ESCI",
    UGC = "UGC", "UGC",
    OTHER = "O", "Other"

class quartile(models.TextChoices):
    Q1 = "Q1", "Q1",
    Q2 = "Q2", "Q2",
    Q3 = "Q3", "Q3",
    Q4 = "Q4", "Q4",
    NA = "NA", "NA"

def rename_journal_file(instance, old_filename):
    extension = os.path.splitext(old_filename)[1].lower()
    username = "".join(map(str.capitalize, instance.email.name.split()))
    new_filename = f"{instance.session}_{username}{extension}"
    return os.path.join('uploads/research_journal/', new_filename)

class research_journal(models.Model):
    @property
    def secure_token(self):
        return jwt.encode(
            {"user_pk": self.pk},
            settings.SECRET_KEY,
            algorithm="HS256"
        )
    noa = models.CharField(max_length=255)
    top = models.CharField(max_length=255)
    noj = models.CharField(max_length=255)
    nop = models.CharField(max_length=255)
    vi = models.CharField(max_length=255)
    pn = models.CharField(max_length=255)
    pd = models.DateField()
    session = models.CharField(
        max_length=7,
        choices=generate_session_choices,
        default=get_current_session
    )
    isnp = models.CharField(max_length=255)
    isno = models.CharField(max_length=255)
    level = models.CharField(
        max_length=2,
        choices=level.choices
    )
    doi = models.CharField(max_length=255)
    lwj = models.URLField(max_length=500)
    lap = models.URLField(max_length=500)
    lrsj = models.URLField(max_length=500)
    aiop = models.CharField(max_length=255)
    ssa = models.CharField(
        max_length=1,
        choices=accept.choices
    )
    details = models.CharField(max_length=255)
    index_by = models.CharField(
        max_length=3,
        choices=index_by.choices
    )
    quartile = models.CharField(
        max_length=2,
        choices=quartile.choices
    )
    proof_file = models.FileField(upload_to=rename_journal_file)
    email = models.ForeignKey(Faculty, on_delete=CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.noj + " " + self.noa

def rename_conference_file(instance, old_filename):
    extension = os.path.splitext(old_filename)[1].lower()
    username = "".join(map(str.capitalize, instance.email.name.split()))
    new_filename = f"{instance.session}_{username}{extension}"
    return os.path.join('uploads/research_conference/', new_filename)

class research_conference(models.Model):
    @property
    def secure_token(self):
        return jwt.encode(
            {"user_pk": self.pk},
            settings.SECRET_KEY,
            algorithm="HS256"
        )
    noa = models.CharField(max_length=255)
    toc = models.CharField(max_length=255)
    top = models.CharField(max_length=255)
    topc = models.CharField(max_length=255)
    level = models.CharField(
        max_length=2,
        choices=level.choices
    )
    isnp = models.CharField(max_length=255)
    nop = models.CharField(max_length=255)
    pd = models.DateField()
    session = models.CharField(
        max_length=7,
        choices=generate_session_choices,
        default=get_current_session
    )
    doi = models.CharField(max_length=255)
    lwj = models.URLField(max_length=500)
    aitp = models.CharField(max_length=255)
    ssa = models.CharField(
        max_length=1,
        choices=accept.choices
    )
    details = models.CharField(max_length=255)
    index_by = models.CharField(max_length=255)
    proof_file = models.FileField(upload_to=rename_conference_file)
    email = models.ForeignKey(Faculty, on_delete=CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.top + " " + self.noa

def rename_book_file(instance, old_filename):
    extension = os.path.splitext(old_filename)[1].lower()
    username = "".join(map(str.capitalize, instance.email.name.split()))
    new_filename = f"{instance.session}_{username}{extension}"
    return os.path.join('uploads/research_book/', new_filename)

class research_book(models.Model):
    @property
    def secure_token(self):
        return jwt.encode(
            {"user_pk": self.pk},
            settings.SECRET_KEY,
            algorithm="HS256"
        )
    noa = models.CharField(max_length=255)
    tob = models.CharField(max_length=255)
    top = models.CharField(max_length=255)
    level = models.CharField(
        max_length=2,
        choices=level.choices
    )
    isbn = models.CharField(max_length=255)
    nop = models.CharField(max_length=255)
    pd = models.DateField()
    session = models.CharField(
        max_length=7,
        choices=generate_session_choices,
        default=get_current_session
    )
    doi = models.CharField(max_length=255)
    lwj = models.URLField(max_length=500)
    aitp = models.CharField(max_length=255)
    ssa = models.CharField(
        max_length=1,
        choices=accept.choices
    )
    details = models.CharField(max_length=255)
    index_by = models.CharField(max_length=255)
    proof_file = models.FileField(upload_to=rename_book_file)
    email = models.ForeignKey(Faculty, on_delete=CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.tob + " "  + self.noa
class type_of_patent(models.TextChoices):
    INNOVATION = "I", "Innovation",
    DESIGN = "D", "Design"

class status_of_patent(models.TextChoices):
    PUBLISHED = "P", "Published",
    GRANTED = "G", "Granted"

def rename_patent_file(instance, old_filename):
    extension = os.path.splitext(old_filename)[1].lower()
    username = "".join(map(str.capitalize, instance.email.name.split()))
    new_filename = f"{instance.session}_{username}_patent{extension}"
    return os.path.join('uploads/patents/', new_filename)

class patents(models.Model):
    @property
    def secure_token(self):
        return jwt.encode(
            {"user_pk": self.pk},
            settings.SECRET_KEY,
            algorithm="HS256"
        )
    sop = models.CharField(
        max_length=1,
        choices=status_of_patent.choices,
        default=status_of_patent.GRANTED
    )
    gi = models.CharField(max_length=255)
    ag = models.CharField(max_length=255)
    top = models.CharField(max_length=255)
    gc = models.CharField(max_length=255)
    pfd = models.DateField(default=datetime.date(2024,1,1))
    pd = models.DateField()
    session = models.CharField(
        max_length=7,
        choices=generate_session_choices,
        default=get_current_session
    )
    pg = models.CharField(
        max_length=1,
        choices=type_of_patent.choices
    )
    ssa = models.CharField(
        max_length=1,
        choices=accept.choices
    )
    details = models.CharField(max_length=255)
    link = models.URLField(max_length=500)
    proof_file = models.FileField(upload_to=rename_patent_file)
    email = models.ForeignKey(Faculty,on_delete=CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.top

class enrollmentYear(models.TextChoices):
    T = '2023', '2023',
    F = '2024', '2024',
    Fi = '2025', '2025'

class survillance(models.TextChoices):
    S = "S", "Supervisor",
    C = "CS", "Co-Supervisor"

class guided(models.Model):
    @property
    def secure_token(self):
        return jwt.encode(
            {"user_pk": self.pk},
            settings.SECRET_KEY,
            algorithm="HS256"
        )
    category = models.CharField(
        max_length=6,
        choices=category.choices,
        default=category.OTHER
    )
    nos = models.CharField(max_length=255)
    ens = models.CharField(max_length=255)
    urns = models.CharField(max_length=255)
    eys = models.CharField(
        max_length=4,
        choices=enrollmentYear.choices
    )
    tod = models.CharField(max_length=255)
    visor = models.CharField(
        max_length=2,
        choices=survillance.choices
    )
    dov = models.DateField()
    noe = models.CharField(max_length=255)
    session = models.CharField(
        max_length=7,
        choices=generate_session_choices,
        default=get_current_session
    )
    email = models.ForeignKey(Faculty,on_delete=CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.get_category_display() + " " + self.nos

class resource_person_type(models.TextChoices):
    EXTERNAL_EXAMINATION_UG = "EE(UG)", "External  Examination(UG)",
    EXTERNAL_EXAMINATION_PG = "EE(PG)", "External  Examination(PG)",
    EDITORIAL_BOARD_MEMBER = "EBM", "Editorial Board Member",
    JURY_MEMBER = "JM", "Jury Member",
    REVIEWER = "R", "Reviewer",
    SESSION_CHAIR = "SC", "Session Chair",
    EXPERT = "E", "Expert",
    SPEAKER = "S", "Speaker",
    KEY_NOTE_SPEAKER = "KNS", "Key Note Speaker",
    TRAINER = "T", "Trainer",
    TECHNICAL_COMMITTEE_MEMBER = "TCM", "Technical Committee Member",
    DELIVERED_INVITED_TALK = "DIT", "Delivered Invited Talk",
    DELIVERED_EXPERT_LECTURE = "DET", "Delivered Expert Lecture",
    BOS_MEMBER = "BM", "BOS Member",
    DRC_MEMBER = "DM", "DRC Member",
    OTHER = "O", "Other"

class resource(models.Model):
    @property
    def secure_token(self):
        return jwt.encode(
            {"user_pk": self.pk},
            settings.SECRET_KEY,
            algorithm="HS256"
        )
    category = models.CharField(
        max_length=6,
        choices=category.choices,
        default=category.OTHER
    )
    toe = models.CharField(max_length=255)
    sa = models.CharField(max_length=200)
    doe = models.IntegerField()
    rpt = models.CharField(
        max_length=6,
        choices=resource_person_type.choices,
        default=resource_person_type.OTHER
    )
    begi_date = models.DateField()
    end_date = models.DateField()
    session = models.CharField(
        max_length=7,
        choices=generate_session_choices,
        default=get_current_session
    )
    venue = models.CharField(max_length=255)
    proof_file = models.FileField(upload_to='uploads/resource/')
    email = models.ForeignKey(Faculty, on_delete=CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.get_category_display() + ": " + self.toe

class designation_non_tech(models.TextChoices):
    OFFICE_ASSISTANT = "OA", "Office Assistant",
    LAB_ASSISTANT = "LA", "Lab Assistant",
    TECHNICAL_ASSISTANT = "TA", "Technical Assistant",
    ASSISTANT = "A", "Assistant",
    CLERK = "C", "Clerk",
    OTHER = "O", "Other"

class professional_course(models.TextChoices):
    CCNA = "CCNA", "CCNA",
    HARWARE_NETWORKING = "HN", "Hardware & Networking",
    LEVEL_0_A = "O/A", "O Level/ A level",
    AWS_CLOUD_TECHNICAL = "ACT", "AWS Cloud Technical",
    VMWARE = "VM", "VMware",
    OTHER = "O", "Other"

class non_teaching_staff(models.Model):
    @property
    def secure_token(self):
        return jwt.encode(
            {"user_pk": self.pk},
            settings.SECRET_KEY,
            algorithm="HS256"
        )
    session = models.CharField(
        max_length=7,
        choices=generate_session_choices,
        default=get_current_session
    )
    name = models.CharField(max_length=255)
    mobile_no = models.CharField(max_length=10)
    email = models.ForeignKey(Faculty,on_delete=models.CASCADE)
    department = models.CharField(
        max_length=8,
        choices=department.choices
    )
    Lab_no = models.CharField(max_length=255)
    designation = models.CharField(
        max_length=2,
        choices= designation_non_tech.choices
    )
    emp_id = models.IntegerField()
    highest_qual = models.CharField(
        max_length=3,
        choices=highest_qual.choices
    )
    university_name = models.CharField(max_length=255)
    pshd = models.IntegerField()
    professional_course = models.JSONField(default=list, blank=True)
    @property
    def professional_display_list(self):
        data = self.professional_course

        # If the database accidentally stored a single string instead of a list
        if isinstance(data, str):
            data = [data]

        # If it's empty or None
        if not data:
            return []

        choice_dict = dict(professional_course.choices)

        # Now 'NTS' stays together as one key
        return ", ".join([choice_dict.get(key, key) for key in data])

    pan_no = models.CharField(max_length=10)
    dob = models.DateField()
    joining_date = models.DateField()
    promotion_date = models.DateField(null=True,blank=True)
    joining_report = models.FileField(upload_to="uploads/non_tech_staff/joining_report/")
    offer_letter = models.FileField(upload_to="uploads/non_tech_staff/offer_letter/")
    higher_degree_certificate = models.FileField(upload_to="uploads/non_tech_staff/higher_degree_certificate/")
    salary_slip = models.FileField(upload_to="uploads/non_tech_staff/salary_slip/",default=None,null = True)
    certificate = models.FileField(upload_to="uploads/non_tech_staff/certificates/",default=None,null = True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name + " " + self.designation
