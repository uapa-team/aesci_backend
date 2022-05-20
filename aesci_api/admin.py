from django.contrib import admin
from .models import Assignment, Admin, Course, GroupCo, GroupStudent, GroupTeacher, Student, Teacher, PairEvaluator, RubricStudentOutcome

# Register your models here.
admin.site.register(Assignment)
admin.site.register(Admin)
admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(PairEvaluator)
admin.site.register(GroupCo)
admin.site.register(GroupStudent)
admin.site.register(GroupTeacher)
admin.site.register(Course)

