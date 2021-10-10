from rest_framework import viewsets, permissions
from rest_framework import status
from rest_framework.response import Response

from ..models import Assignment, Teacher, GroupStudent, Student, AssignmentStudent
from ..serializers import AssignmentSerializer


class AssignmentViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows teachers to create assignments.
    """
    serializer_class = AssignmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.data['role'] == "Student":
            # Return assignments related to Student
            queryset = Assignment.objects.all()
            query_set = queryset.filter(username=self.request.data['username']).order_by('-dateAssignment')
            return query_set

            for element in querysetGS:
                querysetHGS = AssignmentStudent.objects.filter(idGroupStudent=element.id)
                for elementHGS in querysetHGS:
                    groupsList.append(elementHGS.idHomework)

            groupsList.sort(key=lambda x: x.dateAssignment, reverse=True)
            return groupsList

        elif Teacher.objects.filter(username=self.request.data['username']).exists():
            # Return assignments related to Teacher
            return Assignment.objects.all()
