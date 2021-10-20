from rest_framework import viewsets, permissions

from ..models import IndicatorGroup
from ..serializers import IndicatorGroupSerializer

# create indicator group
class IndicatorGroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows admin to create indicator group.
    """
    queryset = IndicatorGroup.objects.all()
    serializer_class = IndicatorGroupSerializer
    permission_classes = [permissions.IsAdminUser]
