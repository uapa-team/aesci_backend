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

from ..models import EvaluationAssignment, IndicatorAssignment, AssignmentStudent, GroupTeacher, GroupStudent
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
        evaluator = self.request.data["evaluator"]

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
            linkPlusFileName = file1['alternateLink'] + ';' + fil.name + ';' + file1['id']
			
            links.append(linkPlusFileName)
            # Remove file from storage
            os.remove(tmp_file)
        
        for i in range(0,len(indicatorsList)):

            #Change grade into measure if the grade is a normal number

            if isNumber == "True" or isNumber == "true":

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
                #print(result1)
                query2=f'SELECT "idAssignmentStudent" FROM aesci_api_assignmentStudent WHERE "Assignment_id" = \'{assignment}\' and "GroupStudent_id" = (SELECT "idGroupStudent" FROM aesci_api_groupstudent WHERE "numGroup_id"=\'{group}\' AND "username_id"=\'{username}\')'
                cursor.execute(query2)
                result2=cursor.fetchone()
                #print(result2)

            IndicatorAssignmentObject = IndicatorAssignment.objects.get(idIndicatorAssignment=result1[0])
            AssignmentStudentObject = AssignmentStudent.objects.get(idAssignmentStudent=result2[0])

            #Create EvaluationStudent objects depending if documents and grades exist

            if links == [] and gradesList == []:
                if (evaluationType == "EVAL") or (evaluationType == "COTE"):
                    evaluator = GroupTeacher.objects.get(idGroupTeacher = evaluator)
                    EvaluationAssignment.objects.create(indicatorAssignment=IndicatorAssignmentObject,
                        assignmentStudent=AssignmentStudentObject,
                        qualifier=qualifier,
                        evaluationType=evaluationType,
                        codeMeasure=measuresList[i],
                        teacherEvaluator=evaluator)
                else:
                    evaluator = GroupStudent.objects.get(idGroupStudent = evaluator)
                    EvaluationAssignment.objects.create(indicatorAssignment=IndicatorAssignmentObject,
                        assignmentStudent=AssignmentStudentObject,
                        qualifier=qualifier,
                        evaluationType=evaluationType,
                        codeMeasure=measuresList[i],
                        studentEvaluator=evaluator)

            elif links == []:
                if (evaluationType == "EVAL") or (evaluationType == "COTE"):
                    evaluator = GroupTeacher.objects.get(idGroupTeacher = evaluator)
                    EvaluationAssignment.objects.create(indicatorAssignment=IndicatorAssignmentObject,
                        assignmentStudent=AssignmentStudentObject,
                        qualifier=qualifier,
                        evaluationType=evaluationType,
                        codeMeasure=measuresList[i],
                        grade=gradesList[i],
                        teacherEvaluator=evaluator)
                else:
                    evaluator = GroupStudent.objects.get(idGroupStudent = evaluator)
                    EvaluationAssignment.objects.create(indicatorAssignment=IndicatorAssignmentObject,
                        assignmentStudent=AssignmentStudentObject,
                        qualifier=qualifier,
                        evaluationType=evaluationType,
                        codeMeasure=measuresList[i],
                        grade=gradesList[i],
                        studentEvaluator=evaluator)

            elif gradesList == []:
                if (evaluationType == "EVAL") or (evaluationType == "COTE"):
                    evaluator = GroupTeacher.objects.get(idGroupTeacher = evaluator)
                    EvaluationAssignment.objects.create(indicatorAssignment=IndicatorAssignmentObject,
                        assignmentStudent=AssignmentStudentObject,
                        qualifier=qualifier,
                        evaluationType=evaluationType,
                        codeMeasure=measuresList[i],
                        documentAttached= links[0],
                        teacherEvaluator=evaluator)
                else:
                    evaluator = GroupStudent.objects.get(idGroupStudent = evaluator)
                    EvaluationAssignment.objects.create(indicatorAssignment=IndicatorAssignmentObject,
                        assignmentStudent=AssignmentStudentObject,
                        qualifier=qualifier,
                        evaluationType=evaluationType,
                        codeMeasure=measuresList[i],
                        documentAttached= links[0],
                        studentEvaluator=evaluator)

            else:
                if (evaluationType == "EVAL") or (evaluationType == "COTE"):
                    evaluator = GroupTeacher.objects.get(idGroupTeacher = evaluator)
                    EvaluationAssignment.objects.create(indicatorAssignment=IndicatorAssignmentObject,
                        assignmentStudent=AssignmentStudentObject,
                        qualifier=qualifier,
                        evaluationType=evaluationType,
                        codeMeasure=measuresList[i],
                        grade=gradesList[i],
                        documentAttached= links[0],
                        teacherEvaluator=evaluator)
                else:
                    evaluator = GroupStudent.objects.get(idGroupStudent = evaluator)
                    EvaluationAssignment.objects.create(indicatorAssignment=IndicatorAssignmentObject,
                        assignmentStudent=AssignmentStudentObject,
                        qualifier=qualifier,
                        evaluationType=evaluationType,
                        codeMeasure=measuresList[i],
                        grade=gradesList[i],
                        documentAttached= links[0],
                        studentEvaluator=evaluator)

        return Response("Calificación exitosa", status=status.HTTP_200_OK)

    def patch(self, request, *args, **kwargs):

        #Get data from request

        qualifier = self.request.data["qualifier"]
        evaluationType = self.request.data["evaluationType"]
        isNumber = self.request.data["isNumber"]
        assignment = self.request.data["assignment"]
        group = self.request.data["group"]
        evaluator = self.request.data["evaluator"]

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
            studentFiles = os.environ.get('EVALUATIONASSIGNMENT_FOLDER')
            # Path to temp file
            tmp_file = os.path.join(settings.MEDIA_ROOT, path)

            # Create File inside folder studentFiles
            file1 = drive.CreateFile({'parents': [{'id': studentFiles}]})
            file1.SetContentFile(path)
            file1.Upload()

            linkPlusFileName = file1['alternateLink'] + ';' + fil.name + ';' + file1['id']
            
            documentsAttached.append(linkPlusFileName)
            # Remove file from storage
            os.remove(tmp_file)

        for i in range(0,len(indicatorsList)):

            # Get partial value
            partial = kwargs.pop('partial', False)

            #Change grade into measure if the grade is a normal number

            if isNumber.lower() == "True".lower():

                if float(gradesList[i]) < 2.1:
                    measuresList.append("1")
                elif float(gradesList[i]) < 3.0:
                    measuresList.append("2")
                elif float(gradesList[i]) < 4.3:
                    measuresList.append("3")
                else:
                    measuresList.append("4")

            #Get the indicatorAsignment and assignmentStudent objects with info from the request
            #Get the current EvaluationAssignment Id to update

            with connection.cursor() as cursor:
                query=f'SELECT "idIndicatorAssignment" FROM aesci_api_indicatorassignment WHERE "assignment_id" = \'{assignment}\' and "indicatorGroup_id" = (SELECT "idIndicatorGroup" FROM aesci_api_indicatorgroup WHERE "numGroup_id"=\'{group}\' AND "performanceIndicator_id"=\'{indicatorsList[i]}\')'
                cursor.execute(query)
                result1=cursor.fetchone()
                #print(result1)
                query2=f'SELECT "idAssignmentStudent" FROM aesci_api_assignmentStudent WHERE "Assignment_id" = \'{assignment}\' and "GroupStudent_id" = (SELECT "idGroupStudent" FROM aesci_api_groupstudent WHERE "numGroup_id"=\'{group}\' AND "username_id"=\'{username}\')'
                cursor.execute(query2)
                result2=cursor.fetchone()
                #print(result2)
                query3=f'SELECT "idEvaluationAssignment" FROM aesci_api_evaluationassignment WHERE "assignmentStudent_id"= \'{result2[0]}\' and "indicatorAssignment_id"=\'{result1[0]}\''
                cursor.execute(query3)
                result3=cursor.fetchone()
                #print(result3)

            instance = EvaluationAssignment.objects.get(pk=result3[0])

            if instance.documentAttached != None:
                link=instance.documentAttached
                #print('a')
                #print(link)
                linkList = list(link.split(";"))
                #print(linkList)
                file1 = drive.CreateFile({'id': linkList[2]})
                file1.Delete()

            if documentsAttached == [] and gradesList == []:
                if (evaluationType == "EVAL") or (evaluationType == "COTE"):
                    #evaluator = GroupTeacher.objects.get(idGroupTeacher = evaluator)
                    data = {"indicatorAssignment":result1[0],
                        "assignmentStudent":result2[0],
                        "qualifier":qualifier,
                        "evaluationType":evaluationType,
                        "codeMeasure":measuresList[i],
                        "teacherEvaluator":evaluator }
                else:
                    #evaluator = GroupStudent.objects.get(idGroupStudent = evaluator)
                    data = {"indicatorAssignment":result1[0],
                        "assignmentStudent":result2[0],
                        "qualifier":qualifier,
                        "evaluationType":evaluationType,
                        "codeMeasure":measuresList[i],
                        "studentEvaluator":evaluator }
            elif documentsAttached == []:
                if (evaluationType == "EVAL") or (evaluationType == "COTE"):
                    #evaluator = GroupTeacher.objects.get(idGroupTeacher = evaluator)
                    data = {"indicatorAssignment":result1[0],
                        "assignmentStudent":result2[0],
                        "qualifier":qualifier,
                        "evaluationType":evaluationType,
                        "codeMeasure":measuresList[i],
                        "grade":gradesList[i],
                        "teacherEvaluator":evaluator }
                else:
                    #evaluator = GroupStudent.objects.get(idGroupStudent = evaluator)
                    data = {"indicatorAssignment":result1[0],
                        "assignmentStudent":result2[0],
                        "qualifier":qualifier,
                        "evaluationType":evaluationType,
                        "codeMeasure":measuresList[i],
                        "grade":gradesList[i],
                        "studentEvaluator":evaluator }
            elif gradesList == []:
                if (evaluationType == "EVAL") or (evaluationType == "COTE"):
                    evaluator = GroupTeacher.objects.get(idGroupTeacher = evaluator)
                    data = {"indicatorAssignment":result1[0],
                        "assignmentStudent":result2[0],
                        "qualifier":qualifier,
                        "evaluationType":evaluationType,
                        "codeMeasure":measuresList[i],
                        "documentAttached": documentsAttached[0],
                        "teacherEvaluator":evaluator }
                else:
                    #evaluator = GroupStudent.objects.get(idGroupStudent = evaluator)
                    data = {"indicatorAssignment":result1[0],
                        "assignmentStudent":result2[0],
                        "qualifier":qualifier,
                        "evaluationType":evaluationType,
                        "codeMeasure":measuresList[i],
                        "documentAttached": documentsAttached[0],
                        "studentEvaluator":evaluator }
            else:
                if (evaluationType == "EVAL") or (evaluationType == "COTE"):
                    #evaluator = GroupTeacher.objects.get(idGroupTeacher = evaluator)
                    data = {"indicatorAssignment":result1[0],
                        "assignmentStudent":result2[0],
                        "qualifier":qualifier,
                        "evaluationType":evaluationType,
                        "codeMeasure":measuresList[i],
                        "grade":gradesList[i],
                        "documentAttached": documentsAttached[0],
                        "teacherEvaluator":evaluator }
                else:
                    #evaluator = GroupStudent.objects.get(idGroupStudent = evaluator)
                    data = {"indicatorAssignment":result1[0],
                        "assignmentStudent":result2[0],
                        "qualifier":qualifier,
                        "evaluationType":evaluationType,
                        "codeMeasure":measuresList[i],
                        "grade":gradesList[i],
                        "documentAttached": documentsAttached[0],
                        "studentEvaluator":evaluator }                        

            #print(data)
            # Set up serializer
            serializer = self.get_serializer(instance, data, partial=partial)
            serializer.is_valid(raise_exception=True)

            # Execute serializer
            self.perform_update(serializer)

        return Response("Actualización exitosa",status=status.HTTP_200_OK)

    def destroy(self, request, pk=None):
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
        #Get the object from the database to delete the files on Drive
        instance = self.get_object()
        link=instance.documentAttached
        if link!=[]:
            #Split the link string to get the Drive Id for the file
            linkList = list(link.split(";"))
            #Get the drive file object using the Id and then delete it
            file1 = drive.CreateFile({'id': linkList[2]})
            file1.Delete()
        instance.delete()       
        return Response("Calificación eliminada exitosamente", status=status.HTTP_200_OK)