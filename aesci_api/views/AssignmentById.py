from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from ..models import Assignment
from ..serializers import AssignmentSerializer

class AssignmentByIdView(APIView):
    """
    Allows to get the relevant information from an assignment using the id as a paramenter
    """
    def get(self, request, *args, **kwargs):
        #Check if the Assignment object exists
        if Assignment.objects.filter(idAssignment=self.request.query_params["id"]).exists():
            #Set up the serializer with the given id. This serializer is a dictionary with other 
            #dictionaries inside it.
            serializer = AssignmentSerializer(Assignment.objects.get(idAssignment=self.request.query_params["id"]))
            #Parses the data given by the serializer.
            res={}
            res['Assignment Id']=serializer.data['idAssignment']
            res['Assignment Name']=serializer.data['nameAssignment']
            res['Assignment Date']=serializer.data['dateAssignment']
            res['Assignment Limit date ']=serializer.data['dateLimitAssignment']
            res['Assignment Description']=serializer.data['description']
            res['Assignment Link']=serializer.data['link']
            #Returns the data
            return Response(res,status=status.HTTP_200_OK)
        #Gives an error mesage if there is not an assignment object with the given Id
        return Response("No se encontró la información",status=status.HTTP_404_NOT_FOUND)