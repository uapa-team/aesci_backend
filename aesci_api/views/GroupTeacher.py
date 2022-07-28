from rest_framework import viewsets, permissions
from rest_framework import status
from rest_framework.response import Response

from ..models import GroupTeacher
from ..serializers import GroupTeacherSerializer


class GroupTeacherViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows admin to create groupTeacher objects.
    """
    queryset = GroupTeacher.objects.all()
    serializer_class = GroupTeacherSerializer
    permission_classes = [permissions.IsAdminUser]
