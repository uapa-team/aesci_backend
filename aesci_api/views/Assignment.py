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
        if Student.objects.filter(username=self.request.data['username']).exists():
        # Return assignments related to Student
            querysetGS = GroupStudent.objects.filter(username=self.request.data['username'])
            groupsList = []

            for element in querysetGS:
                querysetHGS = AssignmentStudent.objects.filter(GroupStudent_id=element.id)
                for elementHGS in querysetHGS:
                    groupsList.append(elementHGS.Assignment)

        # Sort assignment by date
            groupsList.sort(key=lambda x: x.dateAssignment, reverse=True)
            return groupsList

        elif Teacher.objects.filter(username=self.request.data['username']).exists():
            # Return assignments related to Teacher
            return Assignment.objects.all().filter(username=self.request.data['username'])
        return None
