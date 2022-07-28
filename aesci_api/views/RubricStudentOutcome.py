from rest_framework import viewsets, permissions

from ..models import StudentOutcome, Rubric, RubricStudentOutcome
from ..serializers import RubricStudentOutcomeSerializer

from django.db import connection

from rest_framework import status
from rest_framework.response import Response

# create Student Outcomes
class RubricStudentOutcomeViewSet(viewsets.ModelViewSet):
    """
    Acces to the relation between rubrics and student outcomes
    """
    queryset = RubricStudentOutcome.objects.all()
    serializer_class = RubricStudentOutcomeSerializer
    permission_classes = [permissions.IsAdminUser]


	

	
