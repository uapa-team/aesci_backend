from rest_framework import viewsets, permissions

from ..models import IndicatorAssignment
from ..serializers import IndicatorAssignmentSerializer

# create indicator assignment
class IndicatorAssignmentViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows admin to create indicator assignment.
    """
    queryset = IndicatorAssignment.objects.all()
    serializer_class = IndicatorAssignmentSerializer
    permission_classes = [permissions.IsAdminUser]
