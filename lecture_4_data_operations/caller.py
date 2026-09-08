import os
import django
from datetime import date

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import Student

# Run and print your queries

def add_students():
    Student.objects.create(
        student_id='FC5204',
        first_name='John',
        last_name='Doe',
        birth_date='1995-05-15',
        email='john.doe@university.com'
    )

    student_2 = Student()
    student_2.student_id = 'FE0054'
    student_2.first_name = 'Jane'
    student_2.last_name = 'Smith'
    student_2.email = 'jane.smith@university.com'
    student_2.save()

    student_3 = Student(
        student_id='FH2014',
        first_name='Alice',
        last_name='Johnson',
        birth_date='1998-02-10',
        email='alice.johnson@university.com'
    )
    student_3.save()

    Student.objects.create(
        student_id='FH2015',
        first_name='Bob',
        last_name='Wilson',
        birth_date='1996-11-25',
        email='bob.wilson@university.com'
    )

# add_students()
# print(Student.objects.all())

def get_students_info():
    students = []
    for s in Student.objects.all():
        students.append(f'Student №{s.student_id}: {s.first_name} {s.last_name}; Email: {s.email}')

    return '\n'.join(students)

# print(get_students_info())

def update_students_emails():
    students = Student.objects.all()

    for s in students:
        s.email = s.email.replace(s.email.split('@')[1], 'uni-students.com')

    Student.objects.bulk_update(students, ['email'])

# update_students_emails()
# for student in Student.objects.all():
#     print(student.email)

def truncate_students():
    Student.objects.all().delete()

# truncate_students()
# print(Student.objects.all())
# print(f"Number of students: {Student.objects.count()}")