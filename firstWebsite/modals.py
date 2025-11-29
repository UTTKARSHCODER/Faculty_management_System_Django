import datetime
from tkinter.constants import CASCADE

from django.db import models
from django.db.models import DO_NOTHING

class Contact(models.Model):
    first_name = models.CharField(max_length=122)
    last_name = models.CharField(max_length=122)
    email = models.CharField(max_length=122)
    feedback = models.CharField(max_length=122)

class Student_Directory(models.Model):
    name = models.CharField(max_length=100)
    batch = models.CharField(max_length=100,default='Unknown')
    roll_no = models.CharField(max_length=100)
    college_id = models.CharField(max_length=20)
    email = models.EmailField(max_length=254)
    student_phone_no = models.CharField(max_length=10)
    parent_phone_no = models.CharField(max_length=10)
    address = models.TextField()

    def __str__(self):
        return self.name

class sponsors(models.TextChoices):
    SPONSORED = "S", "Sponsored",
    NON_SPONSORED = "NS", "Non-Sponsored"

class session(models.TextChoices):
    Y2025_26 = "2025-26", "2025-26",
    Y2026_27 = "2026-27", "2026-27",
    Y2027_28 = "2027-28", "2027-28",
    Y2028_29 = "2028-29", "2028-29",
    Y2029_30 = "2029-30", "2029-30"

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

class Faculty(models.Model):
    name = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=10)
    email = models.EmailField(max_length=254,unique=True)
    department = models.CharField(
        max_length=8,
        choices=department.choices
    )
    emp_id = models.IntegerField()
    role = models.CharField(
        max_length=3,
        choices=Role.choices,
        default=Role.FACULTY
    )
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
    univ_name = models.CharField(max_length=100,default='Unknown')
    pshd = models.IntegerField(default=0)
    pan_no = models.CharField(max_length=10,default='AAAEE875AE')
    dob = models.DateField()
    jd = models.DateField()
    pd = models.DateField(null=True,blank=True)
    jr = models.FileField(upload_to='uploads/faculty_documents/joining_report/',default=None,null = True)
    of = models.FileField(upload_to='uploads/faculty_documents/offer_letter/',default=None,null = True)
    ss = models.FileField(upload_to='uploads/faculty_documents/salary_slip/',default=None,null = True)
    hdc = models.FileField(upload_to='uploads/faculty_documents/higher_degree_certificate/',default=None,null = True)
    certificate = models.FileField(upload_to='uploads/faculty_documents/certificate/',default=None,null = True)
    phd_univ = models.CharField(max_length=100, null = True, blank = True)
    phd_dor = models.DateField(null=True,blank=True)
    norp = models.IntegerField(default=0)


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
    SHORT_TERM_COURSES = "STC","Short Term Courses",
    MOOC = "MOOC","MOOC courses",
    INDUCTION_PROGRAM = "IP","Induction Program",
    EDUCATION = "EDU","Education",
    RESEARCH = "REA","Research",
    SPORTS = "SPO","Sports",
    SPONSORED_GRANT= "SG","Sponsored Grant",
    RESEARCH_PROJECT = "RP","Research Project",
    CONSULTANCY = "CONS","Consultancy",
    M_TECH = "M_TECH","M.Tech Students",
    PHD = "PH_D","Ph.D Students",
    OTHER = "OTH", "Other"

class Faculty_participation_data(models.Model):
    category = models.CharField(
        max_length=6,
        choices=category.choices,
        default=category.OTHER
    )
    top = models.CharField(max_length=100,default='Unknown')
    mode = models.CharField(
        max_length=2,
        choices=mode.choices
    )
    level = models.CharField(
        max_length=2,
        choices=level.choices
    )
    organizer = models.CharField(max_length=100)
    sponsors = models.CharField(
        max_length=2,
        choices=sponsors.choices
    )
    approval = models.CharField(
        max_length=1,
        choices=accept.choices
    )
    begi_date = models.DateField()
    end_date = models.DateField()
    session = models.CharField(
        max_length=7,
        choices=session.choices
    )
    no_of_days = models.IntegerField()
    proof_enclosed = models.CharField(
        max_length=1,
        choices=accept.choices
    )
    proof_file = models.FileField(upload_to='uploads/fdp_certificate/')
    email = models.ForeignKey(Faculty,on_delete=DO_NOTHING)

    def __str__(self):
        return self.get_category_display() + ": " + self.top

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


class mooc_course(models.Model):
    timeline = models.CharField(max_length=100)
    noc = models.CharField(max_length=100)
    doc = models.CharField(
        max_length=2,
        choices=doc.choices
    )
    begi_date = models.DateField()
    end_date = models.DateField()
    offer = models.CharField(max_length=100)
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
        choices=session.choices
    )
    remarks = models.CharField(max_length=255,null=True)
    proof_file = models.FileField(upload_to='uploads/mooc_certificate/')
    email = models.ForeignKey(Faculty, on_delete=DO_NOTHING)

    def __str__(self):
        return self.noc

class eof(models.TextChoices):
    STUDENTS = "S", "Students",
    TEACHING_STAFF = "TS", "Teaching Staff",
    NON_TEACHING_STAFF = "NTS", "Non-Teaching Staff"

class events(models.Model):
    category = models.CharField(
        max_length=6,
        choices=category.choices,
        default=category.OTHER
    )
    eof = models.CharField(
        max_length=3,
        choices=eof.choices
    )
    topdpo = models.CharField(max_length=100)
    nop = models.IntegerField()
    adcc = models.CharField(max_length=100)
    session = models.CharField(
        max_length=7,
        choices=session.choices
    )
    ct = models.CharField(
        max_length=2,
        choices=sponsors.choices
    )
    nosa = models.CharField(max_length=100)
    cd = models.CharField(max_length=100)
    begi_date = models.DateField()
    end_date = models.DateField()
    gr = models.CharField(
        max_length=1,
        choices=accept.choices
    )
    gd = models.CharField(max_length=100)
    awpsfooe = models.CharField(max_length=100)
    nossp = models.IntegerField()
    nosmp = models.IntegerField()
    eraipf = models.CharField(
        max_length=1,
        choices=accept.choices
    )
    proof_file = models.FileField(upload_to='uploads/events/')
    remarks = models.CharField(max_length=255, null = True)
    email = models.ForeignKey(Faculty, on_delete=DO_NOTHING)

    def __str__(self):
        return self.get_category_display() + " " + self.topdpo

class awards_and_achievments(models.Model):
    category = models.CharField(
        max_length=6,
        choices=category.choices
    )
    noaa = models.CharField(max_length=100)
    paf = models.CharField(max_length=100)
    ao = models.CharField(max_length=100)
    prize = models.CharField(max_length=100)
    ad = models.DateField()
    remark = models.CharField(max_length=255, null = True)
    proof_file = models.FileField(upload_to='uploads/awards/')
    session = models.CharField(
        max_length=7,
        choices=session.choices
    )
    email = models.ForeignKey(Faculty, on_delete=DO_NOTHING)

    def __str__(self):
        return self.get_category_display() + " " + self.noaa

class status(models.TextChoices):
    ONGOING = "ON", "Ongoing",
    COMPLETED = "CM", "Completed"

class sponsored_research(models.Model):
    category = models.CharField(
        max_length=6,
        choices=category.choices
    )
    nofa = models.CharField(max_length=100)
    dop = models.CharField(max_length=100)
    amount = models.IntegerField()
    session = models.CharField(
        max_length=7,
        choices=session.choices
    )
    status = models.CharField(
        max_length=2,
        choices=status.choices
    )
    proof_file = models.FileField(upload_to='uploads/sponsored_research/')
    email = models.ForeignKey(Faculty, on_delete=DO_NOTHING)

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

class research_journal(models.Model):
    noa = models.CharField(max_length=100)
    top = models.CharField(max_length=100)
    noj = models.CharField(max_length=100)
    nop = models.CharField(max_length=100)
    vi = models.CharField(max_length=100)
    pn = models.IntegerField()
    pd = models.DateField()
    session = models.CharField(
        max_length=7,
        choices=session.choices
    )
    isnp = models.CharField(max_length=100)
    isno = models.CharField(max_length=100)
    level = models.CharField(
        max_length=2,
        choices=level.choices
    )
    doi = models.CharField(max_length=100)
    lwj = models.CharField(max_length=100)
    lap = models.CharField(max_length=100)
    lrsj = models.CharField(max_length=100)
    aiop = models.CharField(max_length=100)
    ssa = models.CharField(
        max_length=1,
        choices=accept.choices
    )
    details = models.CharField(max_length=100)
    index_by = models.CharField(
        max_length=3,
        choices=index_by.choices
    )
    quartile = models.CharField(
        max_length=2,
        choices=quartile.choices
    )
    proof_file = models.FileField(upload_to='uploads/research_journal/')
    email = models.ForeignKey(Faculty, on_delete=DO_NOTHING)

    def __str__(self):
        return self.noj + " " + self.noa

class research_conference(models.Model):
    noa = models.CharField(max_length=100)
    toc = models.CharField(max_length=100)
    top = models.CharField(max_length=100)
    topc = models.CharField(max_length=100)
    level = models.CharField(
        max_length=2,
        choices=level.choices
    )
    isnp = models.CharField(max_length=100)
    nop = models.CharField(max_length=100)
    pd = models.DateField()
    session = models.CharField(
        max_length=7,
        choices=session.choices
    )
    doi = models.CharField(max_length=100)
    lwj = models.CharField(max_length=100)
    aitp = models.CharField(max_length=100)
    ssa = models.CharField(
        max_length=1,
        choices=accept.choices
    )
    details = models.CharField(max_length=100)
    index_by = models.CharField(
        max_length=3,
        choices=index_by.choices
    )
    proof_file = models.FileField(upload_to='uploads/research_journal/')
    email = models.ForeignKey(Faculty, on_delete=DO_NOTHING)

    def __str__(self):
        return self.top + " " + self.noa

class research_book(models.Model):
    noa = models.CharField(max_length=100)
    tob = models.CharField(max_length=100)
    top = models.CharField(max_length=100)
    level = models.CharField(
        max_length=2,
        choices=level.choices
    )
    isbn = models.CharField(max_length=100)
    nop = models.CharField(max_length=100)
    pd = models.DateField()
    session = models.CharField(
        max_length=7,
        choices=session.choices
    )
    doi = models.CharField(max_length=255)
    lwj = models.CharField(max_length=255)
    aitp = models.CharField(max_length=100)
    ssa = models.CharField(
        max_length=1,
        choices=accept.choices
    )
    details = models.CharField(max_length=255)
    index_by = models.CharField(
        max_length=3,
        choices=index_by.choices
    )
    proof_file = models.FileField(upload_to="uploads/research_book/")
    email = models.ForeignKey(Faculty, on_delete=DO_NOTHING)

    def __str__(self):
        return self.tob + " "  + self.noa
class type_of_patent(models.TextChoices):
    INNOVATION = "I", "Innovation",
    DESIGN = "D", "Design"

class status_of_patent(models.TextChoices):
    PUBLISHED = "P", "Published",
    GRANTED = "G", "Granted"

class patents(models.Model):
    sop = models.CharField(
        max_length=1,
        choices=status_of_patent.choices,
        default=status_of_patent.GRANTED
    )
    gi = models.CharField(max_length=100)
    ag = models.CharField(max_length=100)
    top = models.CharField(max_length=100)
    gc = models.CharField(max_length=100)
    pfd = models.DateField(default=datetime.date(2024,1,1))
    pd = models.DateField()
    session = models.CharField(
        max_length=7,
        choices=session.choices
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
    link = models.CharField(max_length=255)
    proof_file = models.FileField(upload_to='uploads/patents/')
    email = models.ForeignKey(Faculty,on_delete=DO_NOTHING)

    def __str__(self):
        return self.top

class enrollmentYear(models.TextChoices):
    T = '2023', '2023',
    F = '2024', '2024',
    Fi = '2025', '2025'

class survillance(models.TextChoices):
    S = "S", "Supervisor",
    C = "C", "Co-Supervisor"

class guided(models.Model):
    nos = models.CharField(max_length=100)
    ens = models.CharField(max_length=100)
    urns = models.CharField(max_length=100)
    eys = models.CharField(
        max_length=4,
        choices=enrollmentYear.choices
    )
    tod = models.CharField(max_length=100)
    visor = models.CharField(
        max_length=1,
        choices=survillance.choices
    )
    dov = models.DateField()
    noe = models.CharField(max_length=100)
    session = models.CharField(
        max_length=7,
        choices=session.choices
    )
    email = models.ForeignKey(Faculty,on_delete=DO_NOTHING)

    def __str__(self):
        return self.nos + " " + self.tod

class resouce_person_type(models.TextChoices):
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
    category = models.CharField(
        max_length=6,
        choices=category.choices,
        default=category.OTHER
    )
    toe = models.CharField(max_length=100)
    sa = models.CharField(max_length=200)
    doe = models.IntegerField()
    rpt = models.CharField(
        max_length=6,
        choices=resouce_person_type.choices,
        default=resouce_person_type.OTHER
    )
    begi_date = models.DateField()
    end_date = models.DateField()
    session = models.CharField(
        max_length=7,
        choices=session.choices
    )
    venue = models.CharField(max_length=2550)
    proof_file = models.FileField(upload_to='uploads/resource/')
    email = models.ForeignKey(Faculty, on_delete=DO_NOTHING)

    def __str__(self):
        return self.get_category_display() + ": " + self.toe

class designation_non_tech(models.TextChoices):
    OFFICE_ASSISTANT = "OA", "Office Assistant",
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
    name = models.CharField(max_length=100)
    mobile_no = models.CharField(max_length=10)
    email = models.ForeignKey(Faculty,on_delete=models.CASCADE)
    department = models.CharField(
        max_length=8,
        choices=department.choices
    )
    Lab_no = models.IntegerField()
    designation = models.CharField(
        max_length=2,
        choices= designation_non_tech.choices
    )
    emp_id = models.IntegerField()
    highest_qual = models.CharField(
        max_length=3,
        choices=highest_qual.choices
    )
    university_name = models.CharField(max_length=100)
    pshd = models.IntegerField()
    professional_course = models.CharField(
        max_length=4,
        choices=professional_course.choices
    )
    pan_no = models.CharField(max_length=10)
    dob = models.DateField()
    joining_date = models.DateField()
    promotion_date = models.DateField(null=True,blank=True)
    joining_report = models.FileField(upload_to="uploads/non_tech_staff/joining_report/")
    offer_letter = models.FileField(upload_to="uploads/non_tech_staff/offer_letter/")
    higher_degree_certificate = models.FileField(upload_to="uploads/non_tech_staff/higher_degree_certificate/")
    salary_slip = models.FileField(upload_to="uploads/non_tech_staff/salary_slip/")
    certificate = models.FileField(upload_to="uploads/non_tech_staff/certificates/")

    def __str__(self):
        return self.name + " " + self.designation
