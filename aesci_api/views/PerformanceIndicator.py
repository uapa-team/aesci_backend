from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework import status

from django.db import connection

from ..models import PerformanceIndicator, StudentOutcome
from ..serializers import PerformanceIndicatorSerializer

# create performance indicators
class PerformanceIndicatorViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows admin to create performance indicators.
    """
    queryset = PerformanceIndicator.objects.all()
    serializer_class = PerformanceIndicatorSerializer
    permission_classes = [permissions.IsAdminUser]

    def create(self, request):
        #Get all the data from the request

        codePIRequest = request.data["codePI"]
        descriptionRequest = request.data["description"]
        codeSORequest = request.data["codeSO"]
        isActiveRequest = request.data["isActive"]
    
        with connection.cursor() as cursor:
            #Get the greatest IdPerformanceIndicator to assign the next number to new performanceIndicator
            query='SELECT "idPerformanceIndicator" FROM aesci_api_performanceindicator WHERE "idPerformanceIndicator" = (SELECT max("idPerformanceIndicator") from aesci_api_performanceindicator)'
            cursor.execute(query)
            result=cursor.fetchone()  

		#Get the StudentOutcome with the id
        studentOutcomeObject = StudentOutcome.objects.get(id=codeSORequest)          

        obj, _ = PerformanceIndicator.objects.get_or_create(idPerformanceIndicator=result[0] + 1, codePI=codePIRequest, description=descriptionRequest,
         codeSO=studentOutcomeObject, isActive= isActiveRequest)

        return Response("Indicador creado exitosamente", status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):

        # Get object with pk
        instance = PerformanceIndicator.objects.get(pk=kwargs['pk'])

		#Get all the data from the request

        codePIRequest = request.data["codePI"]
        descriptionRequest = request.data["description"]
        codeSORequest = request.data["codeSO"]  
        isActiveRequest = request.data["isActive"]

        partial = kwargs.pop('partial', False)           		

        data = {"codePI":codePIRequest,"description":descriptionRequest,"codeSO":codeSORequest,"isActive":isActiveRequest}

        # Set up serializer
        serializer = self.get_serializer(instance, data, partial=partial)
        serializer.is_valid(raise_exception=True)
        
        # Execute serializer
        self.perform_update(serializer)

        return Response("Indicador actualizado exitosamente", status=status.HTTP_200_OK)

	#Destroy is, in fact, an Update 
	#We'll update just the value "isActive" and set its value to "False"
    def destroy(self, request, *args, **kwargs):   
		     
        partial = kwargs.pop('partial', False)
        instance = PerformanceIndicator.objects.get(pk=kwargs['pk'])
        data = {"codePI":instance.codePI,"description":instance.description,"codeSO":instance.codeSO_id,"isActive":"False"}

        # Set up serializer
        serializer = self.get_serializer(instance, data, partial=partial)
        serializer.is_valid(raise_exception=True)
        
        # Execute serializer
        self.perform_update(serializer)	                  
        return Response("Indicador eliminado exitosamente", status=status.HTTP_200_OK)
