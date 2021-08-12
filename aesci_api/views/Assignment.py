from rest_framework import viewsets, permissions
from rest_framework import status
from rest_framework.response import Response

from ..models import Assignment, Teacher, GroupStudent, Student, HomeworkGroupStudent
from ..serializers import AssignmentSerializer


class AssignmentViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows teachers to handle assignments.
    """
    serializer_class = AssignmentSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        if Student.objects.filter(username=self.request.data['username']).exists():
        # Return assignments related to Student
            querysetGS = GroupStudent.objects.filter(username=self.request.data['username'])
            groupsList = []

            for element in querysetGS:
                querysetHGS = HomeworkGroupStudent.objects.filter(idGroupStudent=element.id)
                for elementHGS in querysetHGS:
                    groupsList.append(elementHGS.idHomework)

            groupsList.sort(key=lambda x: x.dateAssignment, reverse=True)
            return groupsList

        elif Teacher.objects.filter(username=self.request.data['username']).exists():
            # Return assignments related to Teacher
            return Assignment.objects.all().filter(username=self.request.data['username'])
        return None

    def create(self, request):
        # POST just allowed to Teacher
        if Teacher.objects.filter(username=self.request.data['username']).exists(): 
            # Create assignment
            return super().create(request)
        else:
            return Response("Usuario sin permisos", status=status.HTTP_403_FORBIDDEN)
