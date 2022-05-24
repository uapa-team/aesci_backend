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
        rubrics =''.join(request.data["rubricsList"])
        rubricsString1 = rubrics.replace('[','')
        rubricsString2 = rubricsString1.replace(']','')
        rubricsString3 = rubricsString2.replace('"','')
        rubricsString4 = rubricsString3.replace(' ','')
        rubricsList = list(rubricsString4.split(","))
        isActive = request.data["isActive"]
    	

        with connection.cursor() as cursor:
            #Get the greatest idStudentOutcome to assign the next number to new studentoutcome
            query='SELECT "id" FROM aesci_api_studentoutcome WHERE "id" = (SELECT max("id") from aesci_api_studentoutcome)'
            cursor.execute(query)
            result1=cursor.fetchone()
            query2='SELECT "idRubricStudentOutcome" FROM aesci_api_rubricstudentoutcome WHERE "idRubricStudentOutcome" = (SELECT max("idRubricStudentOutcome") from aesci_api_rubricstudentoutcome)'
            cursor.execute(query2)
            result2=cursor.fetchone()

        try:    
		#Save the idAssignment to later create the assignmentStudent tuple after creating the assignment
            idNewStudentOutcome = result1[0] + 1
        except:
            idNewStudentOutcome = 1

        try:    
		#Save the idAssignment to later create the assignmentStudent tuple after creating the assignment
            idNewRubricStudentOutcome = result2[0] + 1
        except:
            idNewRubricStudentOutcome = 1

        #Create the studentoutcome object in database
        #Create the object in weak entity, too

        obj, _ = StudentOutcome.objects.get_or_create(id=idNewStudentOutcome,description=description,isActive=isActive)
        
        studentOutcomeCreated= StudentOutcome.objects.get(id=idNewStudentOutcome)
        
        count=1

        for i in rubricsList:
            rubricObject = Rubric.objects.get(id=i)
            obj, _ = RubricStudentOutcome.objects.get_or_create(idRubricStudentOutcome=idNewRubricStudentOutcome + count,codeRubric=rubricObject, codeStudentOutcome=studentOutcomeCreated)
            count = count +1

        return Response("Resultado creado exitosamente", status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):

        rubrics =''.join(request.data["rubricsList"])
        rubricsString1 = rubrics.replace('[','')
        rubricsString2 = rubricsString1.replace(']','')
        rubricsString3 = rubricsString2.replace('"','')
        rubricsString4 = rubricsString3.replace(' ','')
        rubricsList = list(rubricsString4.split(","))
        description = request.data["description"]
        isActive = request.data["isActive"]

        partial = kwargs.pop('partial', False)

        instance = StudentOutcome.objects.get(pk=kwargs['pk'])

        data = {"description":description,"isActive":isActive}

        # Set up serializer
        serializer = self.get_serializer(instance, data, partial=partial)
        serializer.is_valid(raise_exception=True)
        
        # Execute serializer
        self.perform_update(serializer)

        #Delete previous relationships between rubric and student outcome
        with connection.cursor() as cursor:
                #Get the RubricStudentOutcome id
                pk=kwargs['pk']
                query=f'DELETE FROM aesci_api_rubricstudentoutcome WHERE "codeStudentOutcome_id"= \'{pk}\''
                cursor.execute(query)
                query2='SELECT "idRubricStudentOutcome" FROM aesci_api_rubricstudentoutcome WHERE "idRubricStudentOutcome" = (SELECT max("idRubricStudentOutcome") from aesci_api_rubricstudentoutcome)'
                cursor.execute(query2)
                result2=cursor.fetchone()

        try:    
		#Save the idAssignment to later create the assignmentStudent tuple after creating the assignment
            idNewRubricStudentOutcome = result2[0] + 1
        except:
            idNewRubricStudentOutcome = 1

        count=0
        
        #Create new relations with data given in the request
        for i in rubricsList:
            rubricObject = Rubric.objects.get(id=i)
            studentOutcomeObject = StudentOutcome.objects.get(id=pk)
            obj, _ = RubricStudentOutcome.objects.get_or_create(idRubricStudentOutcome=idNewRubricStudentOutcome + count,codeRubric=rubricObject, codeStudentOutcome=studentOutcomeObject)
            count = count +1

        return Response("Resultado de formación actualizado", status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):

        partial = kwargs.pop('partial', False)

        instance = StudentOutcome.objects.get(pk=kwargs['pk'])

        data = {"description":instance.description,"isActive":"False"}

        # Set up serializer
        serializer = self.get_serializer(instance, data, partial=partial)
        serializer.is_valid(raise_exception=True)
        
        # Execute serializer
        self.perform_update(serializer)   

        return Response("Resultado de formación inactivo", status=status.HTTP_200_OK)

	

	
