from rest_framework import viewsets, permissions

from ..models import PerformanceIndicator
from ..serializers import PerformanceIndicatorSerializer


class PerformanceIndicatorViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows admin to create performance indicators.
    """
    queryset = PerformanceIndicator.objects.all()
    serializer_class = PerformanceIndicatorSerializer
    permission_classes = [permissions.IsAdminUser]