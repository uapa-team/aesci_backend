from rest_framework import viewsets, permissions

from ..models import StudentOutcome, Rubric
from ..serializers import StudentOutcomeSerializer

from django.db import connection

from rest_framework import status
from rest_framework.response import Response

# create Student Outcomes
class StudentOutcomeViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows admin to create student outcomes.
    """
    queryset = StudentOutcome.objects.all()
    serializer_class = StudentOutcomeSerializer
    permission_classes = [permissions.IsAdminUser]

    def create(self, request):
        
        description = request.data["description"]
        codeRubric = request.data["codeRubric"]
    	

        with connection.cursor() as cursor:
            #Get the greatest idStudentOutcome to assign the next number to new studentoutcome
            query='SELECT "idStudentOutcome" FROM aesci_api_studentoutcome WHERE "idStudentOutcome" = (SELECT max("idStudentOutcome") from aesci_api_studentoutcome)'
            cursor.execute(query)
            result=cursor.fetchone()
        
		#Get the codeRubric object related with the new studentoutcome

        rubric = Rubric.objects.get(idRubric=codeRubric)

        #Create the studentoutcome object in database

        obj, _ = StudentOutcome.objects.get_or_create(idStudentOutcome=result[0] + 1,description=description, codeRubric=rubric)

        return Response("Resultado creado exitosamente", status=status.HTTP_200_OK)

	

	
