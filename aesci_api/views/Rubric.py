from rest_framework import viewsets, permissions,status
from rest_framework.response import Response

from django.db import connection

from ..models import Rubric
from ..serializers import RubricSerializer
from ..helpers import *

# create rubric
class RubricViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows admin to create rubric.
    """
    queryset = Rubric.objects.all()
    serializer_class = RubricSerializer
    permission_classes = [permissions.IsAdminUser]

    def create(self, request, *args, **kwargs):

        codeRubric = request.data["codeRubric"]
        description = request.data["description"]
        isActive = request.data["isActive"]
        
        departmentRubric =''.join(request.data["departmentRubric"])
        departmentRubricString1 = departmentRubric.replace('[','')
        departmentRubricString2 = departmentRubricString1.replace(']','')
        departmentRubricString3 = departmentRubricString2.replace('" ','')
        departmentRubricString4 = departmentRubricString3.replace(' "','')
        departmentRubricString5 = departmentRubricString4.replace('"','')
        departmentRubricList = list(departmentRubricString5.split(","))

        with connection.cursor() as cursor:
            #Get the greatest idRubric to assign the next number to new assignment
            query='SELECT "idRubric" FROM aesci_api_rubric WHERE "idRubric" = (SELECT max("idRubric") from aesci_api_rubric)'
            cursor.execute(query)
            result=cursor.fetchone()

        #departmentCodes = []
#
        #for element0 in departmentRubricList:
        #    for element1 in CARRER_CHOICES:
        #        if element1[1]==element0:
        #            departmentCodes.append(element1[0])

        obj, _ = Rubric.objects.get_or_create(idRubric=result[0] + 1, codeRubric=codeRubric,
        description=description,isActive=isActive, departmentRubric=departmentRubricList)

        return Response("Rúbrica creada", status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):

        codeRubric = request.data["codeRubric"]
        description = request.data["description"]
        isActive = request.data["isActive"]
        
        departmentRubric =''.join(request.data["departmentRubric"])
        departmentRubricString1 = departmentRubric.replace('[','')
        departmentRubricString2 = departmentRubricString1.replace(']','')
        departmentRubricString3 = departmentRubricString2.replace('" ','')
        departmentRubricString4 = departmentRubricString3.replace(' "','')
        departmentRubricString5 = departmentRubricString4.replace('"','')
        departmentRubricList = list(departmentRubricString5.split(","))

        #departmentCodes = []
#
        #for element0 in departmentRubricList:
        #    for element1 in CARRER_CHOICES:
        #        if element1[1]==element0:
        #            departmentCodes.append(element1[0])

        partial = kwargs.pop('partial', False)

        instance = Rubric.objects.get(pk=kwargs['pk'])

        data = {"codeRubric":codeRubric,"description":description,"isActive":isActive,
            "departmentRubric":departmentRubricList}

        # Set up serializer
        serializer = self.get_serializer(instance, data, partial=partial)
        serializer.is_valid(raise_exception=True)
        
        # Execute serializer
        self.perform_update(serializer)

        return Response("Rúbrica actualizada", status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):

        partial = kwargs.pop('partial', False)

        instance = Rubric.objects.get(pk=kwargs['pk'])

        data = {"codeRubric":instance.codeRubric,"description":instance.description,"isActive":"False"}

        # Set up serializer
        serializer = self.get_serializer(instance, data, partial=partial)
        serializer.is_valid(raise_exception=True)
        
        # Execute serializer
        self.perform_update(serializer)   

        return Response("Rúbrica inactiva", status=status.HTTP_200_OK)