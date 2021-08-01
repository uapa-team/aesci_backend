from rest_framework import viewsets, permissions
from rest_framework import status
from rest_framework.response import Response

from ..models import Assignment
from ..serializers import AssignmentSerializer


class AssignmentViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows teachers to create assignments.
    """
    serializer_class = AssignmentSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        if self.request.data['role'] == "Student":
            # Return assignments related to Student
            queryset = Assignment.objects.all()
            query_set = queryset.filter(username=self.request.data['username']).order_by('-dateAssignment')
            return query_set

        elif self.request.data['role'] == "Proffesor":
            # Return assignments related to Teacher
            return Assignment.objects.all()
