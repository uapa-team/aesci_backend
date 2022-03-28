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
        assignment = self.request.data["assignment"]
        group = self.request.data["group"]

        #Create lists for indicators, measures and grades (if they exist)

        indicators =''.join(request.data["indicator"])
        indicatorsString1 = indicators.replace('[','')
        indicatorsString2 = indicatorsString1.replace(']','')
        indicatorsString3 = indicatorsString2.replace('"','')
        indicatorsString4 = indicatorsString3.replace(' ','')
        indicatorsList = list(indicatorsString4.split(","))

        measures =''.join(request.data["measure"])
        measuresString1 = measures.replace('[','')
        measuresString2 = measuresString1.replace(']','')
        measuresString3 = measuresString2.replace('"','')
        measuresString4 = measuresString3.replace(' ','')
        if measuresString4!='':
            measuresList = list(measuresString4.split(","))
        else:
            measuresList = []

        grades =''.join(request.data["grade"])
        gradesString1 = grades.replace('[','')
        gradesString2 = gradesString1.replace(']','')
        gradesString3 = gradesString2.replace('"','')
        gradesString4 = gradesString3.replace(' ','')
        if gradesString4!='':
            gradesList = list(gradesString4.split(","))
        else:
            gradesList = []

        username = self.request.data["studentUsername"]
        files = self.request.FILES.getlist('documentAttached')

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
            file1['title'] = fil.name # Change title of the file.			
            file1.SetContentFile(path)
            file1.Upload()
            
            #print(file1['id'])
            linkPlusFileName = file1['alternateLink'] + ';' + fil.name
			
            links.append(linkPlusFileName)
            # Remove file from storage
            os.remove(tmp_file)
        
        for i in range(0,len(indicatorsList)):

            #Change grade into measure if the grade is a normal number

            if isNumber == "True":

                if float(gradesList[i]) < 2.1:
                    measuresList.append("1")
                elif float(gradesList[i]) < 3.0:
                    measuresList.append("2")
                elif float(gradesList[i]) < 4.3:
                    measuresList.append("3")
                else:
                    measuresList.append("4")

            #Get the indicatorAsignment and assignmentStudent objects with info from the request

            with connection.cursor() as cursor:
                query=f'SELECT "idIndicatorAssignment" FROM aesci_api_indicatorassignment WHERE "assignment_id" = \'{assignment}\' and "indicatorGroup_id" = (SELECT "idIndicatorGroup" FROM aesci_api_indicatorgroup WHERE "numGroup_id"=\'{group}\' AND "performanceIndicator_id"=\'{indicatorsList[i]}\')'
                cursor.execute(query)
                result1=cursor.fetchone()
                print(result1)
                query2=f'SELECT "idAssignmentStudent" FROM aesci_api_assignmentStudent WHERE "Assignment_id" = \'{assignment}\' and "GroupStudent_id" = (SELECT "idGroupStudent" FROM aesci_api_groupstudent WHERE "numGroup_id"=\'{group}\' AND "username_id"=\'{username}\')'
                cursor.execute(query2)
                result2=cursor.fetchone()
                print(result2)

            IndicatorAssignmentObject = IndicatorAssignment.objects.get(idIndicatorAssignment=result1[0])
            AssignmentStudentObject = AssignmentStudent.objects.get(idAssignmentStudent=result2[0])

            #Create EvaluationStudent objects depending if documents and grades exist

            if links == [] and gradesList == []:

                EvaluationAssignment.objects.create(indicatorAssignment=IndicatorAssignmentObject,
                    assignmentStudent=AssignmentStudentObject,
                    qualifier=qualifier,
                    evaluationType=evaluationType,
                    codeMeasure=measuresList[i])

            elif links == []:

                EvaluationAssignment.objects.create(indicatorAssignment=IndicatorAssignmentObject,
                    assignmentStudent=AssignmentStudentObject,
                    qualifier=qualifier,
                    evaluationType=evaluationType,
                    codeMeasure=measuresList[i],
                    grade=gradesList[i])

            elif gradesList == []:

                EvaluationAssignment.objects.create(indicatorAssignment=IndicatorAssignmentObject,
                    assignmentStudent=AssignmentStudentObject,
                    qualifier=qualifier,
                    evaluationType=evaluationType,
                    codeMeasure=measuresList[i],
                    documentAttached= links[0])

            else:

                EvaluationAssignment.objects.create(indicatorAssignment=IndicatorAssignmentObject,
                    assignmentStudent=AssignmentStudentObject,
                    qualifier=qualifier,
                    evaluationType=evaluationType,
                    codeMeasure=measuresList[i],
                    grade=gradesList[i],
                    documentAttached= links[0])

        return Response("Calificación exitosa", status=status.HTTP_200_OK)

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

            linkPlusFileName = file1['alternateLink'] + ';' + fil.name
            
            documentsAttached.append(linkPlusFileName)
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

    def destroy(self, request, pk=None):                   		
        instance = self.get_object()
        instance.delete()                 
            #self.perform_destroy(instance)        
        return Response("Calificación eliminada exitosamente", status=status.HTTP_200_OK)