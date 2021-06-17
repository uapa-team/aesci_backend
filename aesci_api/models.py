from django.db import models
from django.db.models.base import Model
from django.db.models.fields import BigIntegerField, CharField

# URLField ?

# Create your models here.
class Person(models.Model):
    idPerson = models.CharField(max_length = 60)
    role = models.CharField(max_length = 60)
    email = models.CharField(max_length = 60)
    name = models.CharField(max_length = 60)
    class Meta:
        abstract: True

    def __str__(self):
        """String for representing the Model object."""
        return self.name

class Admin(Person):
    charge = models.CharField(max_length = 60)


class Student(Person):
    carrer = models.CharField(max_length = 60)

class Teacher(Person):
    departmentDoc = models.CharField(max_length = 60)

class PairEvaluator(Person):
    institution = models.CharField(max_length = 60)
    
class Assignment(models.Model):
    idAssignment = models.BigIntegerField()
    idDocument = models.BigIntegerField()
    nameAssignament = models.CharField(max_length = 60)
    numGroup = models.BigIntegerField()
    course = models.BigIntegerField()
    codeResult = models.IntegerField()
    dateAssignment = models.DateTimeField()
    dateLimitAssignment = models.DateTimeField()
    description = models.CharField(max_length = 60)
    format = models.CharField(max_length = 60)
    delivery = models.CharField(max_length = 60)
    
    def __str__(self):
        """String for representing the Model object."""
        return self.nameAssignament

class AutoEvaluationCourse(models.Model):
    codeCourse = models.BigIntegerField()
    codeRubric = models.BigIntegerField()
    autoPeriod = models.CharField(max_length = 60)
    idDocument = models.CharField(max_length = 60)
    numberStudents = models.IntegerField()

class CoEvaluation(models.Model):
    codeRubric = models.BigIntegerField()
    studentCOEV = models.BigIntegerField()
    numberGroup = models.BigIntegerField()
    course = models.BigIntegerField()
    documentAttached = models.CharField(max_length = 60)

class Course(models.Model):
    codeCourse = models.BigIntegerField(default=1)
    periodPlan = models.CharField(max_length = 60, default="Test")
    referencePlan = models.IntegerField(default=1)
    nameCourse = models.CharField(max_length = 60,default="Test")
    departmentCourse = models.CharField(max_length = 60, default=1)

    def __str__(self):
        """String for representing the Model object."""
        return self.nameCourse

class EducationResult(models.Model):
    codeResult = models.IntegerField()
    description = models.CharField(max_length = 60)

class GroupCo(models.Model):
    numGroup = models.BigIntegerField()
    course = models.BigIntegerField()

class GroupStudent(models.Model):
    idDocument = models.CharField(max_length = 60)
    numGroup = models.BigIntegerField()
    course = models.BigIntegerField()

class HomeworkStudent(models.Model):
    idDocument = models.CharField(max_length = 60)
    idHomework = models.BigIntegerField()

class ImprovementPlan(models.Model):
    planPeriod = models.CharField(max_length = 60)
    codeResult = models.IntegerField()
    idDocument = models.BigIntegerField()
    diagnosis = models.CharField(max_length = 60)
    analysis = models.CharField(max_length = 60)

class MeasurementEduResult(models.Model):
    measureERPeriod = models.CharField(max_length = 60)
    codeRubric = models.BigIntegerField()
    codeResult = models.IntegerField()
    experts = models.IntegerField()
    competents = models.IntegerField()
    apprentices = models.IntegerField()
    beginners = models.IntegerField()

class MonitoringPlan(models.Model):
    period = models.CharField(max_length=60)
    reference = models.IntegerField()
    idPerson = models.CharField(max_length = 60)
    actions = models.CharField(max_length = 60)
    metodology = models.CharField(max_length = 60)
    courses = models.CharField(max_length = 60)
    progress = models.CharField(max_length = 60)

class Rubric(models.Model):
    codeRubric = models.BigIntegerField()
    rubric = models.JSONField()

class StudentCoEvaluation(models.Model):
    studentCOEV1 = models.BigIntegerField()
    studentCOEV2 = models.BigIntegerField()
    numberGroup = models.BigIntegerField()
    course = models.BigIntegerField()
    codeRubric = models.BigIntegerField()
