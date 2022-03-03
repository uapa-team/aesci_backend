from rest_framework import viewsets, permissions

from ..models import StudentOutcome
from ..serializers import StudentOutcomeSerializer

# create Student Outcomes
class StudentOutcomeViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows admin to create student outcomes.
    """
    queryset = StudentOutcome.objects.all()
    serializer_class = StudentOutcomeSerializer
    permission_classes = [permissions.IsAdminUser]
