from rest_framework import viewsets, permissions
from rest_framework import status
from rest_framework.response import Response

from ..models import GroupStudent
from ..serializers import GroupStudentSerializer


class GroupStudentViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows admin to create groups.
    """
    queryset = GroupStudent.objects.all()
    serializer_class = GroupStudentSerializer
    permission_classes = [permissions.IsAdminUser]