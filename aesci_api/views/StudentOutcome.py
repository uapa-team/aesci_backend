from rest_framework import viewsets, permissions

from ..models import StudentOutcome, Rubric, RubricStudentOutcome
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
        isActive = request.data["isActive"]
    	

        with connection.cursor() as cursor:
            #Get the greatest idStudentOutcome to assign the next number to new studentoutcome
            query='SELECT "id" FROM aesci_api_studentoutcome WHERE "id" = (SELECT max("id") from aesci_api_studentoutcome)'
            cursor.execute(query)
            result=cursor.fetchone()
        
		#Get the codeRubric object related with the new studentoutcome

        rubric = Rubric.objects.get(id=codeRubric)

        #Create the studentoutcome object in database

        objs, _ = StudentOutcome.objects.get_or_create(id=result[0] + 1,description=description,isActive=isActive)

        with connection.cursor() as cursor:
            #Get the greatest idRubricStudentOutcome to assign the next number to new RubricStudentOutcomes raws
            query='SELECT "idRubricStudentOutcome" FROM aesci_api_rubricstudentoutcome WHERE "idRubricStudentOutcome" = (SELECT max("idRubricStudentOutcome") from aesci_api_rubricstudentoutcome)'
            cursor.execute(query)
            result=cursor.fetchone()

        obj, _ = RubricStudentOutcome.objects.get_or_create(idRubricStudentOutcome=result[0] + 1,codeRubric=rubric,codeStudentOutcome=objs)

        return Response("Resultado creado exitosamente", status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):

        codeRubric = request.data["codeRubric"]
        description = request.data["description"]
        isActive = request.data["isActive"]

        partial = kwargs.pop('partial', False)

        instance = StudentOutcome.objects.get(pk=kwargs['pk'])

        data = {"codeRubric":codeRubric,"description":description,"isActive":isActive}

        # Set up serializer
        serializer = self.get_serializer(instance, data, partial=partial)
        serializer.is_valid(raise_exception=True)
        
        # Execute serializer
        self.perform_update(serializer)

        return Response("Resultado de formación actualizado", status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):

        partial = kwargs.pop('partial', False)

        instance = StudentOutcome.objects.get(pk=kwargs['pk'])

        data = {"codeRubric":instance.codeRubric_id,"description":instance.description,"isActive":"False"}

        # Set up serializer
        serializer = self.get_serializer(instance, data, partial=partial)
        serializer.is_valid(raise_exception=True)
        
        # Execute serializer
        self.perform_update(serializer)   

        return Response("Resultado de formación inactivo", status=status.HTTP_200_OK)

	

	
