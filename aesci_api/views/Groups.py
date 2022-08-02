from requests import request
from rest_framework import viewsets, permissions

from ..models import GroupCo, GroupStudent, Student, Teacher, GroupTeacher, Course
from ..serializers import GroupCoSerializer

from rest_framework import status
from rest_framework.response import Response
from ..helpers import PERIODS

from django.db import connection

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

    def create(self, request, *args, **kwargs):
        with connection.cursor() as cursor:
            #Get the greatest idGroupCo to assign the next number to new group
            query='SELECT "idGroupCo" FROM aesci_api_groupco WHERE "idGroupCo" = (SELECT max("idGroupCo") from aesci_api_groupco)'
            cursor.execute(query)
            result=cursor.fetchone()
        idNewGroup = 0
        try:    
            idNewGroup = result[0] + 1
        except:
            idNewGroup = 1
        number = request.data['number']
        courseRequest = request.data['course']
		#We have to see if the course sent exists
        try:
            courseRequest = Course.objects.get(codeCourse=courseRequest)
        except:
            return Response( f'Error: Course code is not valid' , status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        period = request.data['period']
        isPeriodValid = False
        for x in PERIODS:
            if period == x[0]:
                isPeriodValid = True 
                break
        if isPeriodValid == False:
            return Response( f'Period is not valid' , status=status.HTTP_200_OK)
		#Now, let's check if there a group with that number for that course in that period already exists
        try:
            courseRequest = GroupCo.objects.get(course=courseRequest, numGroup=number, periodPlan=period)
            return Response( f'Error: A group with with that number for that course in that period exists already' , status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except:
            obj, _ = GroupCo.objects.get_or_create(idGroupCo=idNewGroup, numGroup=number, course=courseRequest, periodPlan=period)
            return Response( f'Group successfully created' , status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        number = request.data['number']
        courseRequest = request.data['course']
		#We have to see if the course sent exists
        try:
            courseRequest = Course.objects.get(codeCourse=courseRequest)
        except:
            return Response( f'Error: Course code is not valid' , status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        period = request.data['period']
        isPeriodValid = False
        for x in PERIODS:
            if period == x[0]:
                isPeriodValid = True 
                break
        if isPeriodValid == False:
            return Response( f'Period is not valid' , status=status.HTTP_200_OK)
		#Now, let's check if there a group with that number for that course in that period already exists
        try:
            courseRequest = GroupCo.objects.get(course=courseRequest, numGroup=number, periodPlan=period)
            return Response( f'Error: A group with with that number for that course in that period exists already' , status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except:
            partial = kwargs.pop('partial', False)
    
            instance = GroupCo.objects.get(pk=kwargs['pk'])
    
            data = {"numGroup":number,"course":courseRequest.codeCourse,"periodPlan":period}
    
            # Set up serializer
            serializer = self.get_serializer(instance, data, partial=partial)
            serializer.is_valid(raise_exception=True)
            
            # Execute serializer
            self.perform_update(serializer)
            return Response( f'Group successfully updated' , status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):

        instance = GroupCo.objects.get(pk=kwargs['pk'])
        instance.delete() 

        return Response("Group successfully deleted", status=status.HTTP_200_OK)
