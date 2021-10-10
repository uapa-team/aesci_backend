from rest_framework import viewsets, permissions
from rest_framework import status
from rest_framework.response import Response

from ..models import Course, GroupCo, GroupStudent, GroupTeacher
from ..serializers import GroupTeacherSerializer


class GroupTeacherViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows admin to create groups.
    """
    queryset = GroupTeacher.objects.all()
    serializer_class = GroupTeacherSerializer
    permission_classes = [permissions.IsAdminUser]
