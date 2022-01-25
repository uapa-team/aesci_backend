from rest_framework import viewsets, permissions
from rest_framework import status
from rest_framework.response import Response

from ..models import Assignment, Teacher, GroupStudent, Student, AssignmentStudent
from ..serializers import AssignmentSerializer


class AssignmentViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows teachers to create assignments.
    """
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer
    permission_classes = [permissions.AllowAny]

    # def get_queryset(self, pk=None):
    #     if Teacher.objects.filter(username=self.request.query_params["username"]).exists():
    #         # Return assignments related to Teacher
    #         return Assignment.objects.filter(username=self.request.query_params["username"])
    #     return Assignment.objects.all() 
