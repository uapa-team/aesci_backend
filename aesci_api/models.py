from django.db import models
from django.db.models.base import Model
from django.db.models.fields import BigIntegerField, CharField
from django.contrib.auth.models import User, Group

# URLField ?

# Create your models here.
class Admin(models.Model):
    username = models.CharField(max_length = 60, primary_key=True)
    idPerson = models.CharField(max_length = 60)
    email = models.CharField(max_length = 60)
    name = models.CharField(max_length = 60)
    charge = models.CharField(max_length = 60)

    def save(self, *args, **kwargs):
        user = User.objects.create(username = self.username, is_staff = True, is_superuser = True)
        my_group = Group.objects.get(name='Admin') 
        my_group.user_set.add(user)
        super(Admin, self).save(*args, **kwargs)

    def __str__(self):
        """String for representing the Model object."""
        return self.username
    
class Student(models.Model):
    username = models.CharField(max_length = 60, primary_key=True)
    idPerson = models.CharField(max_length = 60)
    email = models.CharField(max_length = 60)
    name = models.CharField(max_length = 60)
    carrer = models.CharField(max_length = 60)

    def save(self, *args, **kwargs):
        user = User.objects.create(username = self.username )
        my_group = Group.objects.get(name='Student') 
        my_group.user_set.add(user)
        super(Student, self).save(*args, **kwargs)

    def __str__(self):
        """String for representing the Model object."""
        return self.username

class Teacher(models.Model):
    username = models.CharField(max_length = 60, primary_key=True)
    idPerson = models.CharField(max_length = 60)
    email = models.CharField(max_length = 60)
    name = models.CharField(max_length = 60)
    departmentDoc = models.CharField(max_length = 60)

    def save(self, *args, **kwargs):
        user = User.objects.create(username = self.username )
        my_group = Group.objects.get(name='Teacher') 
        my_group.user_set.add(user)
        super(Teacher, self).save(*args, **kwargs)

    def __str__(self):
        """String for representing the Model object."""
        return self.username

class PairEvaluator(models.Model):
    username = models.CharField(max_length = 60, primary_key=True)
    idPerson = models.CharField(max_length = 60)
    email = models.CharField(max_length = 60)
    name = models.CharField(max_length = 60)
    institution = models.CharField(max_length = 60)

    def save(self, *args, **kwargs):
        user = User.objects.create(username = self.username )
        my_group = Group.objects.get(name='PairEvaluator') 
        my_group.user_set.add(user)
        super(PairEvaluator, self).save(*args, **kwargs)

    def __str__(self):
        """String for representing the Model object."""
        return self.username

class Course(models.Model):
    codeCourse = models.BigIntegerField(default=1, primary_key=True)
    referencePlan = models.IntegerField(default=1)
    nameCourse = models.CharField(max_length = 60,default="Test")
    departmentCourse = models.CharField(max_length = 60, default=1)

    def __str__(self):
        """String for representing the Model object."""
        return self.nameCourse

class EducationResult(models.Model):
    codeResult = models.IntegerField(primary_key=True)
    description = models.CharField(max_length = 60)

class GroupCo(models.Model):
    numGroup = models.BigIntegerField(primary_key=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    periodPlan = models.CharField(max_length = 60, default="Test")

    def __str__(self):
        """String for representing the Model object."""
        return self.course.nameCourse

class GroupStudent(models.Model):
    username = models.ForeignKey(Student, on_delete=models.CASCADE)
    numGroup = models.ForeignKey(GroupCo, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

class GroupTeacher(models.Model):
    username = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    numGroup = models.ForeignKey(GroupCo, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

class Rubric(models.Model):
    codeRubric = models.BigIntegerField(primary_key=True)
    rubric = models.JSONField()
    
class Assignment(models.Model):
    idAssignment = models.BigIntegerField(primary_key=True)
    username = models.ForeignKey(Student, on_delete=models.CASCADE)
    nameAssignament = models.CharField(max_length = 60)
    numGroup = models.ForeignKey(GroupCo, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    codeResult = models.ForeignKey(EducationResult, on_delete=models.CASCADE)
    dateAssignment = models.DateTimeField()
    dateLimitAssignment = models.DateTimeField()
    description = models.CharField(max_length = 60)
    formatAssignment = models.CharField(max_length = 60)
    delivery = models.CharField(max_length = 60)
    
    def __str__(self):
        """String for representing the Model object."""
        return self.nameAssignament

class AutoEvaluationCourse(models.Model):
    codeCourse = models.ForeignKey(Course, on_delete=models.CASCADE)
    codeRubric = models.ForeignKey(Rubric, on_delete=models.CASCADE)
    autoPeriod = models.CharField(max_length = 60)
    username = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    numberStudents = models.IntegerField()

class CoEvaluation(models.Model):
    codeRubric = models.ForeignKey(Rubric, on_delete=models.CASCADE)
    studentCOEV2 = models.ForeignKey(Student, on_delete=models.CASCADE)
    numberGroup = models.ForeignKey(GroupCo, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    documentAttached = models.CharField(max_length = 60)

class StudentCoEvaluation(models.Model):
    studentCOEV1 = models.ForeignKey(Student, on_delete=models.CASCADE)
    studentCOEV2 = models.ForeignKey(CoEvaluation, on_delete=models.CASCADE)
    numberGroup = models.ForeignKey(GroupCo, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    codeRubric = models.ForeignKey(Rubric, on_delete=models.CASCADE)

class HomeworkStudent(models.Model):
    username = models.ForeignKey(Student, on_delete=models.CASCADE)
    idHomework = models.ForeignKey(Assignment, on_delete=models.CASCADE)

class ImprovementPlan(models.Model):
    planPeriod = models.CharField(max_length = 60)
    codeResult = models.ForeignKey(EducationResult, on_delete=models.CASCADE)
    username = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    diagnosis = models.CharField(max_length = 60)
    analysis = models.CharField(max_length = 60)

class MeasurementEduResult(models.Model):
    measureERPeriod = models.CharField(max_length = 60)
    codeRubric = models.ForeignKey(Rubric, on_delete=models.CASCADE)
    codeResult = models.ForeignKey(EducationResult, on_delete=models.CASCADE)
    experts = models.IntegerField()
    competents = models.IntegerField()
    apprentices = models.IntegerField()
    beginners = models.IntegerField()

class MonitoringPlan(models.Model):
    period = models.CharField(max_length=60)
    reference = models.ForeignKey(EducationResult, on_delete=models.CASCADE)
    username = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    actions = models.CharField(max_length = 60)
    metodology = models.CharField(max_length = 60)
    courses = models.CharField(max_length = 60)
    progress = models.CharField(max_length = 60)