from rest_framework import viewsets, permissions

from ..models import StudentOutcome, Rubric, RubricStudentOutcome
from ..serializers import StudentOutcomeSerializer

from django.db import connection

from rest_framework import status
from rest_framework.response import Response

# create Student Outcomes
class RubricsStudentOutcomeViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows admin to create student outcomes.
    """
    queryset = RubricStudentOutcome.objects.all()

	

	
