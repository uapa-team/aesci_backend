from django.contrib import admin
from .models import Assignment, Admin, Student, Teacher, PairEvaluator

# Register your models here.
admin.site.register(Assignment)
admin.site.register(Admin)
admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(PairEvaluator)
