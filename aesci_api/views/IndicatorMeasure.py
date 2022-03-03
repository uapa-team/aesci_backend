from rest_framework import viewsets, permissions

from ..models import IndicatorMeasure
from ..serializers import IndicatorMeasureSerializer

# create indicator measure
class IndicatorMeasureViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows admin to create indicator measure.
    """
    queryset = IndicatorMeasure.objects.all()
    serializer_class = IndicatorMeasureSerializer
    permission_classes = [permissions.IsAdminUser]
