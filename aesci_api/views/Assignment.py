from rest_framework import viewsets, permissions
from rest_framework import status
from rest_framework.response import Response

<<<<<<< HEAD
from ..models import Assignment, Teacher, GroupStudent, Student
=======
from ..models import Assignment
>>>>>>> ab4c73c7ffdc7bd570930ccc23abe366df374ebc
from ..serializers import AssignmentSerializer


class AssignmentViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows teachers to handle assignments.
    """
    serializer_class = AssignmentSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        # if self.request.data['role'] == "Student":
        # if Student.objects.filter(username=self.request.data['username']).exists():
        # #     # Return assignments related to Student
        #     queryset1 = GroupStudent.objects.filter(username=self.request.data['username'])
        # for element in queryset1:
        # 
        #     queryset2 = Assignment.objects.filter(username=self.request.data['username'])
        # #     query_set = queryset.filter(idGroupStudent=?).order_by('-dateAssignment')
        #     return query_set

        # elif self.request.data['role'] == "Proffesor":
        if Teacher.objects.filter(username=self.request.data['username']).exists():
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
