from rest_framework import viewsets, permissions

from ..models import GroupCo, GroupStudent, Student, Teacher, GroupTeacher
from ..serializers import GroupCoSerializer

#create groups
class GroupCoViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows admin to create groups.
    """
    # queryset = GroupCo.objects.all()
    serializer_class = GroupCoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self, pk=None):
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

        return GroupStudent.objects.all() 
