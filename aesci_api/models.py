from django.db import models
from django.db.models.base import Model
from django.db.models.fields import BigIntegerField, CharField

# URLField ?

# Create your models here.
class Person(models.Model):
    idPerson = models.CharField()
    role = models.CharField()
    email = models.CharField()
    name = models.CharField()
class Admin(Person):
    charge = models.CharField()

class Student(Person):
    carrer = models.CharField()

class Teacher(Person):
    departmentDoc = models.CharField()

class PairEvaluator(Person):
    institution = models.CharField()
class Assignment(models.Model):
    idAssignment = models.BigIntegerField()
    idDocument = models.BigIntegerField()
    nameAssignament = models.CharField()
    numGroup = models.BigIntegerField()
    course = models.BigIntegerField()
    codeResult = models.IntegerField()
    dateAssignment = models.DateTimeField()
    dateLimitAssignment = models.DateTimeField()
    description = models.CharField()
    format = models.CharField()
    delivery = models.CharField()

class AutoEvaluationCourse(models.Model):
    codeCourse = models.BigIntegerField()
    codeRubric = models.BigIntegerField()
    autoPeriod = models.CharField()
    idDocument = models.CharField()()
    numberStudents = models.IntegerField()

class CoEvaluation(models.Model):
    codeRubric = models.BigIntegerField()
    studentCOEV = models.BigIntegerField()
    numberGroup = models.BigIntegerField()
    course = models.BigIntegerField()
    documentAttached = models.CharField()

class Course(models.Model):
    codeCourse = models.BigIntegerField()
    periodPlan = models.CharField()
    referencePlan = models.IntegerField()
    nameCourse = models.CharField()(max_length = 60)
    departmentCourse = models.CharField()

    def __str__(self):
        return self.nameCourse

class EducationResult(models.Model):
    codeResult = models.IntegerField()
    description = models.CharField()

class Group(models.Model):
    numGroup = models.BigIntegerField()
    course = models.BigIntegerField()

class GroupStudent(models.Model):
    idDocument = models.CharField()()
    numGroup = models.BigIntegerField()
    course = models.BigIntegerField()

class HomeworkStudent(models.Model):
    idDocument = models.CharField()()
    idHomework = models.BigIntegerField()

class ImprovementPlan(models.Model):
    planPeriod = models.CharField()
    codeResult = models.IntegerField()
    idDocument = models.BigIntegerField()
    diagnosis = models.CharField()
    analysis = models.CharField()

class MeasurementEduResult(models.Model):
    measureERPeriod = models.CharField()
    codeRubric = models.BigIntegerField()
    codeResult = models.IntegerField()
    experts = models.IntegerField()
    competents = models.IntegerField()
    apprentices = models.IntegerField()
    beginners = models.IntegerField()

class MonitoringPlan(models.Model):
    period = CharField()
    reference = models.IntegerField()
    idPerson = models.CharField()
    actions = models.CharField()
    metodology = models.CharField()
    courses = models.CharField()
    progress = models.CharField()

class Rubric(models.Model):
    codeRubric = models.BigIntegerField()
    rubric = models.JSONField()

class StudentCoEvaluation(models.Model):
    studentCOEV1 = models.BigIntegerField()
    studentCOEV2 = models.BigIntegerField()
    numberGroup = models.BigIntegerField()
    course = models.BigIntegerField()
    codeRubric = models.BigIntegerField()
