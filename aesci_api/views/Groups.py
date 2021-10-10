from rest_framework import viewsets, permissions

from ..models import Course, GroupCo
from ..serializers import GroupCoSerializer

#create groups
class GroupCoViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows admin to create groups.
    """
    queryset = GroupCo.objects.all()
    serializer_class = GroupCoSerializer
    permission_classes = [permissions.IsAdminUser]
