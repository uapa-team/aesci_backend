from requests import request
from rest_framework import viewsets, permissions

from ..models import GroupCo, GroupStudent, Student, Teacher, GroupTeacher
from ..serializers import GroupCoSerializer

from rest_framework import status
from rest_framework.response import Response

#create groups
class GroupCoViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows admin to create groups.
    """
    serializer_class = GroupCoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self, pk=None):
        if self.request.method == 'GET' and 'username' in self.request.GET:
            if GroupStudent.objects.filter(username=self.request.query_params["username"]).exists():
                # Return groups where student is avalaible 
                    queryGroups = GroupStudent.objects.filter(username=self.request.query_params["username"])
                    groupstudent = []
                    for group in queryGroups:
                        groupstudent.append(group.numGroup)
                    return groupstudent
            elif GroupTeacher.objects.filter(username=self.request.query_params["username"]).exists():
                # Return groups where teacher is related 
                    queryGroups = GroupTeacher.objects.filter(username=self.request.query_params["username"])
                    groupteacher = []
                    for group in queryGroups:
                        groupteacher.append(group.numGroup)
                    return groupteacher
        elif self.request.method == 'GET' and 'id' in self.request.GET:
            return GroupCo.objects.filter(idGroupCo=self.request.query_params["id"])
        else:
            #return GroupStudent.objects.all()
            return GroupCo.objects.all()

    def post(self, request, *args, **kwargs):
        number = request.data['number']
        course = request.data['course']
        period = request.data['period']
        return Response( f'Group created' , status=status.HTTP_200_OK)

