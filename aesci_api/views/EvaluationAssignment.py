import os
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile


from ..models import EvaluationAssignment, IndicatorAssignment
from ..serializers import EvaluationAssignmentSerializer
from ..helpers import EVTYPES

# create evaluation to assignments
class EvaluationAssignmentViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows admin to create evaluation to assignments.
    """
    queryset = EvaluationAssignment.objects.all()
    serializer_class = EvaluationAssignmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request):
        #print(self.request.query_params["isNumber"])
        documentsAttached = self.request.FILES.get('documentAttached')
		#documentsAttached = self.request.data["documentAttached"]
        grade = self.request.data["grade"]
        indicatorAssignment = IndicatorAssignment.objects.get(idIndicatorAssignment = self.request.data["indicatorAssignment_id"])
        evaluationType = self.request.data["evaluationType"]
        qualifier = self.request.data["qualifier"]

        if documentsAttached is None:
            if float(grade) < 2.1:
                codeMeasure = "1"
            elif float(grade) < 3.0:
                codeMeasure = "2"
            elif float(grade) < 4.3:
                codeMeasure = "3"
            else:
                codeMeasure = "4"

            EvaluationAssignment.objects.create(qualifier= qualifier, codeMeasure=codeMeasure, grade=grade, indicatorAssignment=indicatorAssignment, evaluationType=evaluationType)
        else:
            
            path = default_storage.save("tmp", ContentFile(documentsAttached.read()))
            gauth = GoogleAuth()
            gauth.LoadCredentialsFile("./aesci_api/views/credentials.json")
            if gauth.credentials is None:
                # Authenticate if they're not there
                gauth.LocalWebserverAuth()
            elif gauth.access_token_expired:
                gauth.Refresh()
            else: 
                gauth.Authorize()
            drive = GoogleDrive(gauth)
            # Set up folder ID                         
            evaluationAssignment = os.environ.get('EVALUATIONASSIGNMENT_FOLDER')
            # Path to temp file
            tmp_file = os.path.join(settings.MEDIA_ROOT, path)
            # Create File inside folder evaluationAssignment
            file1 = drive.CreateFile({'parents': [{'id': evaluationAssignment}]})
            file1.SetContentFile(path)
            file1.Upload()
            
            # Remove file from storage
            os.remove(tmp_file)                                    

            EvaluationAssignment.objects.create(documentAttached= file1['id'], grade= grade, qualifier= qualifier, codeMeasure=self.request.data["codeMeasure"], indicatorAssignment=indicatorAssignment, evaluationType=evaluationType)

        return Response( status=status.HTTP_200_OK)

	#This is not done yet
    def update(self, request, *args, **kwargs):
        files = request.FILES.getlist('file')
        documentsAttached = []

        for fil in files:
            path = default_storage.save("tmp", ContentFile(fil.read()))

            gauth = GoogleAuth()
            gauth.LoadCredentialsFile("./aesci_api/views/credentials.json")
            if gauth.credentials is None:
                # Authenticate if they're not there
                gauth.LocalWebserverAuth()
            elif gauth.access_token_expired:
                gauth.Refresh()
            else: 
                gauth.Authorize()

            drive = GoogleDrive(gauth)

            # Set up folder ID 
            studentFiles = os.environ.get('ASSIGNMENT_FOLDER')
            # Path to temp file
            tmp_file = os.path.join(settings.MEDIA_ROOT, path)

            # Create File inside folder studentFiles
            file1 = drive.CreateFile({'parents': [{'id': studentFiles}]})
            file1.SetContentFile(path)
            file1.Upload()
            
            documentsAttached.append(file1['id'])
            # Remove file from storage
            os.remove(tmp_file)

        # Get partial value
        partial = kwargs.pop('partial', False)
        
        # Get object with pk
		#PROBABLY PROBLEM HERE
        instance = self.get_object()

        # Merge old documentsAttached  with new ones        
        if instance.documentAttached is None:
            data = documentsAttached
        else:
            data = instance.documentAttached + documentsAttached
        data = { "documentAttached":data }
        
        # Set up serializer
        serializer = self.get_serializer(instance, data, partial=partial)
        serializer.is_valid(raise_exception=True)
        
        # Execute serializer
        self.perform_update(serializer)

        return Response(serializer.data)




