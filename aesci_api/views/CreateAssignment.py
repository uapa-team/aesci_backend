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

from ..models import Assignment, Teacher, GroupCo, IndicatorAssignment, IndicatorGroup, AssignmentStudent, GroupStudent

class CreateAssignmentView(APIView):

    def post(self, request, *args, **kwargs):

        #Get all the data from the request

        name = request.data["nameAssignment"]
        date = request.data["dateAssignment"]
        dateLimit = request.data["dateLimitAssignment"]
        description = request.data["description"]
        numGroup = request.data["numGroup"]
        teacher = request.data["usernameTeacher"]

        indicators =''.join(request.data["idIndicators"])
        indicatorsString1 = indicators.replace('[','')
        indicatorsString2 = indicatorsString1.replace(']','')
        indicatorsString3 = indicatorsString2.replace('"','')
        indicatorsString4 = indicatorsString3.replace(' ','')
        indicatorsList = list(indicatorsString4.split(","))
        
        files = self.request.FILES.getlist('file')
        print(files)
        
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
            assignmentFiles = os.environ.get('ASSIGNMENT_FOLDER')
            # Path to temp file
            tmp_file = os.path.join(settings.MEDIA_ROOT, path)                        

            # Create File inside folder assignmentFiles
            file1 = drive.CreateFile({'parents': [{'id': assignmentFiles}]})
            file1['title'] = fil.name # Change title of the file.
            file1.SetContentFile(path)
            file1.Upload()

            linkPlusFileName = file1['alternateLink'] + ';' + fil.name

            #print(file1['id'])
            links.append(linkPlusFileName)
#            print(file1)
            # Remove file from storage
            os.remove(tmp_file)

        #Get teacher and group objects to create assignment instance later
        
        #print("A")

        teacherObject = Teacher.objects.get(username=teacher)
        groupObject = GroupCo.objects.get(idGroupCo=numGroup)

        #Conusult the database

        indicatorGroup_list = []

        #print("B")

        with connection.cursor() as cursor:
            #Get the greatest idAssignment to assign the next number to new assignment
            query='SELECT "idAssignment" FROM aesci_api_assignment WHERE "idAssignment" = (SELECT max("idAssignment") from aesci_api_assignment)'
            cursor.execute(query)
            result=cursor.fetchone()
            #print("C")
            #print(result)
            #Get the indicatorGroup id with the group and indicators ids
            for i in indicatorsList:
                query2=f'SELECT "idIndicatorGroup" FROM aesci_api_indicatorgroup WHERE "performanceIndicator_id" = \'{i}\' and "numGroup_id" = \'{numGroup}\''
                cursor.execute(query2)
                result2 = cursor.fetchone()
                indicatorGroup_list.append(result2)
            
        try:    
		#Save the idAssignment to later create the assignmentStudent tuple after creating the assignment
            idNewAssignment = result[0] + 1
        except:
            idNewAssignment = 1

        #Create the assignment object in database
        #print("D")
        if links == []:
            obj, _ = Assignment.objects.get_or_create(idAssignment=idNewAssignment,usernameTeacher=teacherObject, nameAssignment=name,
         numGroup=groupObject, dateAssignment=date, dateLimitAssignment=dateLimit, description=description)
        else:
            obj, _ = Assignment.objects.get_or_create(idAssignment=idNewAssignment ,usernameTeacher=teacherObject, nameAssignment=name,
         numGroup=groupObject, dateAssignment=date, dateLimitAssignment=dateLimit, description=description, link=links)
        
        #Create the indicatorAssignment objects in database

        assignmentObject = Assignment.objects.get(idAssignment=idNewAssignment)
        #print("E")
        for element in indicatorGroup_list:
            indicatorGroupObject = IndicatorGroup.objects.get(idIndicatorGroup=element[0])
            obj, _ = IndicatorAssignment.objects.get_or_create(indicatorGroup=indicatorGroupObject,assignment=assignmentObject)

		#Create the assignmentStudent objects in database
        
        maxIdAssignmentStudent = []
        idGroupStudent_list = []

        with connection.cursor() as cursor:
            #Get the greatest idAssignment to assign the next number to new assignment
            query='SELECT "idAssignmentStudent" FROM aesci_api_assignmentstudent WHERE "idAssignmentStudent" = (SELECT max("idAssignmentStudent") from aesci_api_assignmentstudent)'
            cursor.execute(query)
            maxIdAssignmentStudent=cursor.fetchone()
            try:
                maxIdAssignmentStudent=maxIdAssignmentStudent[0]
            except:
                maxIdAssignmentStudent=0
            #print("F")
            #print(maxIdAssignmentStudent)

            #Get the idGroupStudent of tuples from aesci_api_groupstudent whose attribute numGroup_id has the value
			#numGroup sent via the request 
            
            query2=f'SELECT "idGroupStudent" FROM aesci_api_groupstudent WHERE "numGroup_id" = \'{numGroup}\''
            cursor.execute(query2)            
            idGroupStudent_list = cursor.fetchall()		

		#for each valua in idGroupStudent_list create a raw in the table aesci_api_assignmentstudent
				        
        for groupStudent in idGroupStudent_list:
            maxIdAssignmentStudent = maxIdAssignmentStudent+1				
            groupStudent = GroupStudent.objects.get(idGroupStudent=groupStudent[0])                
            obj, _ = AssignmentStudent.objects.get_or_create(idAssignmentStudent=maxIdAssignmentStudent+1, GroupStudent=groupStudent,Assignment=assignmentObject)        

        return Response("Tarea creada exitosamente", status=status.HTTP_200_OK)
        