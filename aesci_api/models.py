from django.db import models
from django.db.models.base import Model
from django.db.models.fields import BigIntegerField, CharField
from django.contrib.auth.models import User, Group
from django.contrib.postgres.fields import ArrayField
from django.utils.timezone import now
from .helpers import CARRER_CHOICES, MEASURES, EVTYPES

# URLField ?

# Create your models here.
class Admin(models.Model):
    username = models.CharField(max_length = 60, primary_key=True)
    Person = models.CharField(max_length = 60)
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
    Person = models.CharField(max_length = 60)
    email = models.CharField(max_length = 60)
    name = models.CharField(max_length = 60)
    carrer = models.CharField(max_length = 60, choices = CARRER_CHOICES)

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
    Person = models.CharField(max_length = 60)
    email = models.CharField(max_length = 60)
    name = models.CharField(max_length = 60)
    departmentDoc = models.CharField(max_length = 60)

    def save(self, *args, **kwargs):
        user = User.objects.create(username = self.username )
        my_group = Group.objects.get(name='Professor') 
        my_group.user_set.add(user)
        super(Teacher, self).save(*args, **kwargs)

    def __str__(self):
        """String for representing the Model object."""
        return self.username

class PairEvaluator(models.Model):
    username = models.CharField(max_length = 60, primary_key=True)
    Person = models.CharField(max_length = 60)
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

class GroupCo(models.Model):
    numGroup = models.BigIntegerField(primary_key=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    periodPlan = models.CharField(max_length = 60, default="Test")
    def __str__(self):
        """String for representing the Model object."""
        return self.course.nameCourse

class Rubric(models.Model):
    codeRubric = models.BigIntegerField(primary_key=True)
    description = models.CharField(max_length = 60, null = True)

class StudentOutcome(models.Model):
    codeRubric = models.ForeignKey(Rubric, on_delete=models.CASCADE)
    description = models.CharField(max_length = 100)
    def __str__(self):
        """String for representing the Model object."""
        return self.description

class Assignment(models.Model):
    idAssignment = models.AutoField(primary_key=True)
    username = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    nameAssignament = models.CharField(max_length = 60)
    numGroup = models.ForeignKey(GroupCo, on_delete=models.CASCADE)
    dateAssignment = models.DateTimeField(default=now)
    dateLimitAssignment = models.DateTimeField(default=now)
    description = models.CharField(max_length = 60)
    
    def __str__(self):
        """String for representing the Model object."""
        return self.nameAssignament

class GroupStudent(models.Model):
    username = models.ForeignKey(Student, on_delete=models.CASCADE)
    numGroup = models.ForeignKey(GroupCo, on_delete=models.CASCADE)

class GroupTeacher(models.Model):
    username = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    numGroup = models.ForeignKey(GroupCo, on_delete=models.CASCADE)

class HomeworkGroupStudent(models.Model):
    Homework = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    GroupStudent = models.ForeignKey(GroupStudent, on_delete=models.CASCADE, default=None)
    grade = models.FloatField(default=None, null=True)
    link = ArrayField(
        ArrayField(
            models.URLField(max_length=200),
            size=8,
        ),
        size=8,
        null=True
    )

class ImprovementPlan(models.Model):
    planPeriod = models.CharField(max_length = 60)
    codeResult = models.ForeignKey(StudentOutcome, on_delete=models.CASCADE)
    username = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    diagnosis = models.CharField(max_length = 60)
    analysis = models.CharField(max_length = 60)

class MonitoringPlan(models.Model):
    period = models.CharField(max_length=60)
    reference = models.ForeignKey(StudentOutcome, on_delete=models.CASCADE)
    username = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    actions = models.CharField(max_length = 60)
    metodology = models.CharField(max_length = 60)
    courses = models.CharField(max_length = 60)
    progress = models.CharField(max_length = 60)

class PerformanceIndicator(models.Model):
    codeSO = models.ForeignKey(StudentOutcome, on_delete=models.CASCADE)
    description = models.CharField(max_length = 100)

class IndicatorGroup(models.Model):
    performanceIndicator = models.ForeignKey(PerformanceIndicator, on_delete=models.CASCADE)
    numGroup = models.ForeignKey(GroupCo, on_delete=models.CASCADE)

class IndicatorAssignment(models.Model):
    indicatorGroup = models.ForeignKey(IndicatorGroup, on_delete=models.CASCADE)
    homework = models.ForeignKey(HomeworkGroupStudent, on_delete=models.CASCADE)

class IndicatorMeasure(models.Model):
    performanceIndicator = models.ForeignKey(PerformanceIndicator, on_delete=models.CASCADE)
    codeMeasure = models.CharField(
        max_length=1,
        choices=MEASURES,
    )
    description = models.CharField(max_length = 60)
    

class AutoEvaluationCourse(models.Model):
    codeCourse = models.ForeignKey(Course, on_delete=models.CASCADE)
    codeRubric = models.ForeignKey(Rubric, on_delete=models.CASCADE)
    autoPeriod = models.CharField(max_length = 60)
    username = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    numberStudents = models.IntegerField()

class EvaluationAssignment(models.Model):
    indicatorAssignment = models.ForeignKey(IndicatorAssignment, on_delete=models.CASCADE)
    qualifier = models.CharField(max_length = 60)
    documentAttached = models.URLField(max_length=200)
    evaluationType = models.CharField(
        max_length=4,
        choices=EVTYPES,
    )
    codeMeasure = models.CharField(
        max_length=1,
        choices=MEASURES,
    )
    
