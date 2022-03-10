import os
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

from django.db import connection

from ..models import EvaluationAssignment, IndicatorAssignment, AssignmentStudent
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

        #Get data from request
        
        qualifier = self.request.data["qualifier"]
        evaluationType = self.request.data["evaluationType"]
        isNumber = self.request.data["isNumber"]
        grade = self.request.data["grade"]
        measure = self.request.data["measure"]
        assignment = self.request.data["assignment"]
        group = self.request.data["group"]
        indicator = self.request.data["indicator"]
        username = self.request.data["studentUsername"]
        files = self.request.FILES.getlist('documentAttached')
        

        #Change grade into measure if the grade is a normal number

        if isNumber == "True":

            if float(grade) < 2.1:
                codeMeasure = "1"
            elif float(grade) < 3.0:
                codeMeasure = "2"
            elif float(grade) < 4.3:
                codeMeasure = "3"
            else:
                codeMeasure = "4"

        #Get the indicatorAsignment and assignmentStudent objects with info from the request

        with connection.cursor() as cursor:
            query=f'SELECT "idIndicatorAssignment" FROM aesci_api_indicatorassignment WHERE "assignment_id" = \'{assignment}\' and "indicatorGroup_id" = (SELECT "idIndicatorGroup" FROM aesci_api_indicatorgroup WHERE "numGroup_id"=\'{group}\' AND "performanceIndicator_id"=\'{indicator}\')'
            cursor.execute(query)
            result1=cursor.fetchone()
            print(result1)
            query2=f'SELECT "idAssignmentStudent" FROM aesci_api_assignmentStudent WHERE "Assignment_id" = \'{assignment}\' and "GroupStudent_id" = (SELECT "idGroupStudent" FROM aesci_api_groupstudent WHERE "numGroup_id"=\'{group}\' AND "username_id"=\'{username}\')'
            cursor.execute(query)
            result2=cursor.fetchone()
            print(result2)

        IndicatorAssignmentObject = IndicatorAssignment.objects.get(idIndicatorAssignment=result1[0])
        AssignmentStudentObject = AssignmentStudent.objects.get(idAssignmentStudent=result2[0])

        links = []

        #Upload files to Google Drive

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
            studentFiles = os.environ.get('EVALUATIONASSIGNMENT_FOLDER')
            # Path to temp file
            tmp_file = os.path.join(settings.MEDIA_ROOT, path)

            # Create File inside folder studentFiles
            file1 = drive.CreateFile({'parents': [{'id': studentFiles}]})
            file1.SetContentFile(path)
            file1.Upload()
            
            print(file1['id'])
            links.append(file1['id'])
            # Remove file from storage
            os.remove(tmp_file)


        #Create EvaluationStudent objects

        if links == []:

            EvaluationAssignment.objects.create(indicatorAssignment=IndicatorAssignmentObject,
                assignmentStudent=AssignmentStudentObject,
                qualifier=qualifier,
                evaluationType=evaluationType,
                codeMeasure=codeMeasure,
                grade=grade)
        
        else:
                                                
            EvaluationAssignment.objects.create(indicatorAssignment=IndicatorAssignmentObject,
                assignmentStudent=AssignmentStudentObject,
                qualifier=qualifier,
                evaluationType=evaluationType,
                codeMeasure=codeMeasure,
                grade=grade,
                documentAttached= links[0])

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




