from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from ..models import AssignmentStudent
from ..serializers import AssignmentStudentSerializer

class AssignmentStudentByIdView(APIView):
    """
    Allows to get the relevant information from an assignmentStudent using the id as a paramenter
    """
    def get(self, request, *args, **kwargs):
        #Check if the AssignmentStudent object exists
        if AssignmentStudent.objects.filter(idAssignmentStudent=self.request.query_params["id"]).exists():
            #Set up the serializer with the given id. This serializer is a dictionary with other 
            #dictionaries inside it.
            serializer = AssignmentStudentSerializer(AssignmentStudent.objects.get(idAssignmentStudent=self.request.query_params["id"]))
            #Parses the data given by the serializer.
            res={}
            res['Assignment Id']=serializer.data['Assignment']['idAssignment']
            res['Assignment Name']=serializer.data['Assignment']['nameAssignment']
            res['Assignment Date']=serializer.data['Assignment']['dateAssignment']
            res['Assignment Limit date ']=serializer.data['Assignment']['dateLimitAssignment']
            res['Assignment Description']=serializer.data['Assignment']['description']
            res['Assignment Link']=serializer.data['Assignment']['link']
            res['Response Link']=serializer.data['link']
            res['Teacher Name']=serializer.data['Assignment']['usernameTeacher']['name']
            res['Teacher username']=serializer.data['Assignment']['usernameTeacher']['username']
            res['Student Name']=serializer.data['GroupStudent']['username']['name']
            res['Student Username']=serializer.data['GroupStudent']['username']['username']
            #Returns the data
            return Response(res,status=status.HTTP_200_OK)
        #Gives an error mesage if there is not an assignmentStudent object with the given Id
        return Response("No se encontró la información",status=status.HTTP_404_NOT_FOUND)