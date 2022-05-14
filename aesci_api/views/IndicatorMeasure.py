from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework import status

from django.db import connection

from ..models import IndicatorMeasure, PerformanceIndicator
from ..serializers import IndicatorMeasureSerializer

# create indicator measure
class IndicatorMeasureViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows admin to create indicator measure.
    """
    queryset = IndicatorMeasure.objects.all()
    serializer_class = IndicatorMeasureSerializer
    permission_classes = [permissions.IsAdminUser]

    def create(self, request):
        #Get all the data from the request

        indicators =''.join(request.data["performanceIndicator"])
        indicatorsString1 = indicators.replace('[','')
        indicatorsString2 = indicatorsString1.replace(']','')
        indicatorsString3 = indicatorsString2.replace('"','')
        indicatorsString4 = indicatorsString3.replace(' ','')
        indicatorsList = list(indicatorsString4.split(","))
        descriptionRequest = request.data["description"]
        codeMeasureRequest = request.data["codeMeasure"]        
        levelRequest = request.data["level"]		
    
        for i in indicatorsList:
            with connection.cursor() as cursor:
                #Get the greatest idIndicatorMeasure to assign the next number to new indicatorMeasure
                query='SELECT "idIndicatorMeasure" FROM aesci_api_indicatormeasure WHERE "idIndicatorMeasure" = (SELECT max("idIndicatorMeasure") from aesci_api_indicatormeasure)'
                cursor.execute(query)
                result=cursor.fetchone()  

            #Get the PerformanceIndicator with the id
            performanceIndicatorObject = PerformanceIndicator.objects.get(idPerformanceIndicator=i)          

            obj, _ = IndicatorMeasure.objects.get_or_create(idIndicatorMeasure=result[0] + 1, performanceIndicator=performanceIndicatorObject, description=descriptionRequest,
            codeMeasure=codeMeasureRequest, levelMeasure=levelRequest)

        return Response("Medida del indicador creada exitosamente", status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):

        # Get object with pk
        instance = IndicatorMeasure.objects.get(pk=kwargs['pk'])

		#Get all the data from the request

        performanceIndicatorRequest = request.data["performanceIndicator"]
        descriptionRequest = request.data["description"]
        codeMeasureRequest = request.data["codeMeasure"]
        levelRequest = request.data["level"]		 

        partial = kwargs.pop('partial', False)           
		

        data = {"performanceIndicator":performanceIndicatorRequest,"description":descriptionRequest,"codeMeasure":codeMeasureRequest,"levelMeasure":levelRequest}

        # Set up serializer
        serializer = self.get_serializer(instance, data, partial=partial)
        serializer.is_valid(raise_exception=True)
        
        # Execute serializer
        self.perform_update(serializer)

        return Response("Medida de indicador actualizada exitosamente", status=status.HTTP_200_OK)
	
    def destroy(self, request, *args, **kwargs):   
		     
        partial = kwargs.pop('partial', False)
        instance = IndicatorMeasure.objects.get(pk=kwargs['pk'])
        instance.delete()
        return Response("Medida de indicador eliminada exitosamente", status=status.HTTP_200_OK)
