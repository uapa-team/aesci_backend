import os

from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

from django.db import connection

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

from ..models import Assignment, Teacher, GroupCo, IndicatorAssignment, IndicatorGroup

class CreateAssignmentView(APIView):

    def post(self, request, *args, **kwargs):

        #Get all the data from the request

        name = request.data["nameAssignment"]
        date = request.data["dateAssignment"]
        dateLimit = request.data["dateLimitAssignment"]
        description = request.data["description"]
        numGroup = request.data["numGroup"]
        teacher = request.data["usernameTeacher"]

        indicators = request.data["idIndicators"]
        indicatorsList = list(indicators.split(","))
        
        files = request.FILES.getlist('file')
        
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
            studentFiles = os.environ.get('ASSIGNMENT_FOLDER')
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

        #Get teacher and group objects to create assignment instance later
        
        print("A")

        teacherObject = Teacher.objects.get(username=teacher)
        groupObject = GroupCo.objects.get(idGroupCo=numGroup)

        #Conusult the database

        indicatorGroup_list = []

        print("B")

        with connection.cursor() as cursor:
            #Get the greatest idAssignment to assign the next number to new assignment
            query='SELECT "idAssignment" FROM aesci_api_assignment WHERE "idAssignment" = (SELECT max("idAssignment") from aesci_api_assignment)'
            cursor.execute(query)
            result=cursor.fetchone()
            print("C")
            print(result)
            #Get the indicatorGroup id with the group and indicators ids
            for i in indicatorsList:
                query2=f'SELECT "idIndicatorGroup" FROM aesci_api_indicatorgroup WHERE "performanceIndicator_id" = \'{i}\' and "numGroup_id" = \'{numGroup}\''
                cursor.execute(query2)
                result2 = cursor.fetchone()
                indicatorGroup_list.append(result2)
            
        #Create the assignment object in database
        print("D")
        if links == []:
            obj, _ = Assignment.objects.get_or_create(idAssignment=result[0] + 1,usernameTeacher=teacherObject, nameAssignment=name,
         numGroup=groupObject, dateAssignment=date, dateLimitAssignment=dateLimit, description=description)
        else:
            obj, _ = Assignment.objects.get_or_create(idAssignment=result[0] + 1 ,usernameTeacher=teacherObject, nameAssignment=name,
         numGroup=groupObject, dateAssignment=date, dateLimitAssignment=dateLimit, description=description, link=links)
        
        #Create the indicatorAssignment objects in database

        assignmentObject = Assignment.objects.get(idAssignment=result[0] + 1)
        print("E")
        for element in indicatorGroup_list:
            indicatorGroupObject = IndicatorGroup.objects.get(idIndicatorGroup=element[0])
            obj, _ = IndicatorAssignment.objects.get_or_create(indicatorGroup=indicatorGroupObject,assignment=assignmentObject)

        return Response("Tarea creada exitosamente", status=status.HTTP_200_OK)
        