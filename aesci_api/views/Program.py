from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework import status

from django.db import connection

from ..models import Program
from ..serializers import ProgramSerializer

# create indicator measure
class ProgramViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows admin to create indicator measure.
    """
    queryset = Program.objects.all()
    serializer_class = ProgramSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request):
        #Get all the data from the request

        idProgram = request.data["idProgram"]
        name = request.data["name"]
        aims =''.join(request.data["aims"])
        aims1 = aims.replace('{','')
        aims2 = aims1.replace('}','')
        aims3 = aims2.replace(' ',' ')
        aims4 = aims3.replace('"','')
        aims = list(aims4.split(";"))
        learningOutcomes =''.join(request.data["learningOutcomes"])
        learningOutcomes1 = learningOutcomes.replace('{','')
        learningOutcomes2 = learningOutcomes1.replace('}','')
        learningOutcomes3 = learningOutcomes2.replace(' ',' ')
        learningOutcomes4 = learningOutcomes3.replace('"','')
        learningOutcomes = list(learningOutcomes4.split(";"))
        matrix = request.data["matrix"]	
    
        obj, _ = Program.objects.get_or_create(idProgram=idProgram, name=name, aims=aims,
         learningOutcomes=learningOutcomes, matrix=matrix)

        return Response("Programa creado exitosamente", status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):

        # Get object with pk
        instance = Program.objects.get(pk=kwargs['pk'])

		#Get all the data from the request

        name = request.data["name"]
        aims =''.join(request.data["aims"])
        aims1 = aims.replace('{','')
        aims2 = aims1.replace('}','')
        aims3 = aims2.replace(' ',' ')
        aims4 = aims3.replace('"','')
        aims = list(aims4.split(";"))
        learningOutcomes =''.join(request.data["learningOutcomes"])
        learningOutcomes1 = learningOutcomes.replace('{','')
        learningOutcomes2 = learningOutcomes1.replace('}','')
        learningOutcomes3 = learningOutcomes2.replace(' ',' ')
        learningOutcomes4 = learningOutcomes3.replace('"','')
        learningOutcomes = list(learningOutcomes4.split(";"))
        matrix = request.data["matrix"]		 

        partial = kwargs.pop('partial', False)           
		

        data = {"name":name,"aims":aims,"learningOutcomes":learningOutcomes,"matrix":matrix}

        # Set up serializer
        serializer = self.get_serializer(instance, data, partial=partial)
        serializer.is_valid(raise_exception=True)
        
        # Execute serializer
        self.perform_update(serializer)

        return Response("Programa actualizado exitosamente", status=status.HTTP_200_OK)
	
    def destroy(self, request, *args, **kwargs):   
		     
        partial = kwargs.pop('partial', False)
        instance = Program.objects.get(pk=kwargs['pk'])
        instance.delete()
        return Response("Programa eliminado exitosamente", status=status.HTTP_200_OK)
