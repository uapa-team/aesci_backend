from rest_framework import viewsets, permissions
from rest_framework import status
from rest_framework.response import Response

from ..models import Course, GroupCo, GroupStudent, GroupTeacher
from ..serializers import GroupStudentSerializer


class GroupStudentViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows admin to create groups.
    """
    queryset = GroupStudent.objects.all()
    serializer_class = GroupStudentSerializer
    permission_classes = [permissions.AllowAny]

    # def get_queryset(self):
    #     if self.request.data['role'] == "Student":

    #         # Return groups related to Student
    #         queryset = GroupStudent.objects.all()
    #         query_set = queryset.filter(username=self.request.data['username']).order_by('-course_id')
    #         return query_set

    #     elif self.request.data['role'] == "Proffesor":
    #         # Return groups related to Teacher
    #         return GroupTeacher.objects.all()
