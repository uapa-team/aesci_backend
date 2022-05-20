from ast import Or
from tokenize import group
from numpy import int64
import pandas 
import os
import numpy as np

from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

from django.db import connection

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


from ..models import Rubric, StudentOutcome, PerformanceIndicator, IndicatorMeasure, RubricStudentOutcome, Course, GroupCo, IndicatorGroup
# Create your views here.

class UploadRubricsView(APIView):
    """Create student's users"""
    def post(self, request, *args, **kwargs):
        file = request.FILES['file']
        path = default_storage.save("tmp", ContentFile(file.read()))
        
        data_frame_rubricsInfo = pandas.read_excel(path, sheet_name='Rubrica')
       # Filter columns we need and then turn them into lists
        rubricsCode = data_frame_rubricsInfo['RubricCode'].tolist()
        rubricsDescription = data_frame_rubricsInfo['RubricName'].tolist()
        studentOutcomesDescription = data_frame_rubricsInfo['StudentOutcome'].tolist()
        PerformanceIndicatorsCode = data_frame_rubricsInfo['PerformanceIndicatorCode'].tolist()
        PerformanceIndicatorsDescription = data_frame_rubricsInfo['PerformanceIndicatorDescription'].tolist()
        IndicatorMeasuresDescription = data_frame_rubricsInfo['IndicatorMeasureDescription'].tolist()		

        with connection.cursor() as cursor:
            #Get the greatest idAssignment to assign the next number to new assignment
            query='SELECT "id" FROM aesci_api_rubric WHERE "id" = (SELECT max("id") from aesci_api_rubric)'
            cursor.execute(query)
            result=cursor.fetchone()

        try:
            greatestRubricId = result[0]	
        except:
            greatestRubricId = 0	
        createdRubricsCounter = 0
        createdRubricsInfo = []
        for i in range(len(rubricsCode)):	
            if pandas.isnull(rubricsCode[i]) != True:
                createdRubricsCounter += 1						
                obj, _ = Rubric.objects.get_or_create(id=greatestRubricId + (createdRubricsCounter), codeRubric=rubricsCode[i], description=rubricsDescription[i],isActive='True',departmentRubric=['2549'])
                createdRubricsInfo.append((greatestRubricId + createdRubricsCounter))

        with connection.cursor() as cursor:
            #Get the greatest idAssignment to assign the next number to new assignment
            query='SELECT "id" FROM aesci_api_studentoutcome WHERE "id" = (SELECT max("id") from aesci_api_studentoutcome)'
            cursor.execute(query)
            result=cursor.fetchone()

        try:
            greatestStudentOutcomeId = result[0]	
        except:
            greatestStudentOutcomeId = 0	

        with connection.cursor() as cursor:
            #Get the greatest idRubricStudentOutcome to assign the next number to new RubricStudentOutcomes raws
            query='SELECT "idRubricStudentOutcome" FROM aesci_api_rubricstudentoutcome WHERE "idRubricStudentOutcome" = (SELECT max("idRubricStudentOutcome") from aesci_api_rubricstudentoutcome)'
            cursor.execute(query)
            result=cursor.fetchone()


        currentRubric = 0
        try:
            currentRubricStudentOutcome = result[0]
        except:
            currentRubricStudentOutcome = 0	        
        createdStudentOutcomesCounter = 0
        createdStudentOutcomeInfo = []
        for i in range(len(studentOutcomesDescription)):			
            if pandas.isnull(studentOutcomesDescription[i]) != True:
                currentRubricStudentOutcome += 1
                createdStudentOutcomesCounter += 1
                if pandas.isnull(rubricsCode[i]) != True:
                    currentRubric += 1
                    #create the weak entity 
                #now student outcome won't take the id of the rubric but of the weak entity
                currentRubricObject = Rubric.objects.get(id=createdRubricsInfo[currentRubric-1])
                obj, _ = StudentOutcome.objects.get_or_create(id=greatestStudentOutcomeId + (createdStudentOutcomesCounter), isActive='True', description=studentOutcomesDescription[i])
				#Create weak entity
                obj, _ = RubricStudentOutcome.objects.get_or_create(idRubricStudentOutcome=currentRubricStudentOutcome, codeRubric=currentRubricObject, codeStudentOutcome= obj)
                createdStudentOutcomeInfo.append((greatestStudentOutcomeId + createdStudentOutcomesCounter))
            else:
                if pandas.isnull(rubricsCode[i]) != True:
                    currentRubric += 1
                    currentRubricStudentOutcome += 1
                    currentRubricObject = Rubric.objects.get(id=createdRubricsInfo[currentRubric-1])
                    currentStudentOutcomeObject = StudentOutcome.objects.get(id=greatestStudentOutcomeId + (createdStudentOutcomesCounter))
                    obj, _ = RubricStudentOutcome.objects.get_or_create(idRubricStudentOutcome=currentRubricStudentOutcome, codeRubric=currentRubricObject, codeStudentOutcome= currentStudentOutcomeObject)
                    #create week entity using current rubric and current studentOutcome
	

        with connection.cursor() as cursor:
            #Get the greatest idAssignment to assign the next number to new assignment
            query='SELECT "idPerformanceIndicator" FROM aesci_api_performanceindicator WHERE "idPerformanceIndicator" = (SELECT max("idPerformanceIndicator") from aesci_api_performanceindicator)'
            cursor.execute(query)
            result=cursor.fetchone()

        currentStudentOutcome = 0
        try:
            greatestPerformanceIndicatorId = result[0]
        except:
            greatestPerformanceIndicatorId = 0	                
        createdPerformanceIndicatorsCounter = 0
        createdPerformanceIndicatorInfo = []
        for i in range(len(PerformanceIndicatorsCode)):			
            if pandas.isnull(PerformanceIndicatorsCode[i]) != True:
                createdPerformanceIndicatorsCounter += 1
                if pandas.isnull(studentOutcomesDescription[i]) != True:
                    currentStudentOutcome += 1
                currentStudentOutcomeObject = StudentOutcome.objects.get(id=createdStudentOutcomeInfo[currentStudentOutcome-1])
                obj, _ = PerformanceIndicator.objects.get_or_create(idPerformanceIndicator=greatestPerformanceIndicatorId + (createdPerformanceIndicatorsCounter), codeSO=currentStudentOutcomeObject, codePI= PerformanceIndicatorsCode[i], description=PerformanceIndicatorsDescription[i], isActive='True')
                createdPerformanceIndicatorInfo.append((greatestPerformanceIndicatorId + createdPerformanceIndicatorsCounter))

        with connection.cursor() as cursor:
            #Get the greatest idAssignment to assign the next number to new assignment
            query='SELECT "idIndicatorMeasure" FROM aesci_api_indicatormeasure WHERE "idIndicatorMeasure" = (SELECT max("idIndicatorMeasure") from aesci_api_indicatormeasure)'
            cursor.execute(query)
            result=cursor.fetchone()

        currentPerformanceIndicator = 0
        try:
            greatestIndicatorMeasureId = result[0]
        except:
            greatestIndicatorMeasureId = 0
        createdIndicatorMeasuresCounter = 0
        currentCodeMeasure = 4
        currentLevelMeasure = 'Experto'
        for i in range(len(IndicatorMeasuresDescription)):			
            if pandas.isnull(IndicatorMeasuresDescription[i]) != True:
                createdIndicatorMeasuresCounter += 1
                if pandas.isnull(PerformanceIndicatorsCode[i]) != True:
                    currentPerformanceIndicator += 1
                    currentCodeMeasure = 4
                    currentLevelMeasure = 'Experto'
                else:
                    currentCodeMeasure -= 1
                    if currentCodeMeasure == 3:
                        currentLevelMeasure = 'Competente'
                    elif currentCodeMeasure == 2:
                        currentLevelMeasure = 'Aprendiz'
                    elif currentCodeMeasure == 1:
                        currentLevelMeasure = 'Novato'
                currentPerformanceIndicatorObject = PerformanceIndicator.objects.get(idPerformanceIndicator=createdPerformanceIndicatorInfo[currentPerformanceIndicator-1])
                obj, _ = IndicatorMeasure.objects.get_or_create(idIndicatorMeasure=greatestIndicatorMeasureId + (createdIndicatorMeasuresCounter), performanceIndicator=currentPerformanceIndicatorObject, codeMeasure= currentCodeMeasure, levelMeasure = currentLevelMeasure, description=IndicatorMeasuresDescription[i])

		#Now that we've finished creating the rubrics, student outcomes, performances indicators and indicators meausres
		#we'll create the rows that relate the courses with the performanceIndicators 
        data_frame_courseInfo = pandas.read_excel(path, sheet_name='Asignatura')

#       # Filter columns we need and then turn them into lists
        program = data_frame_courseInfo['Program'].tolist()
        courseCode = data_frame_courseInfo['CourseCode'].tolist()
        courseName = data_frame_courseInfo['CourseName'].tolist()
        indicatorsCode = data_frame_courseInfo['IndicatorsCode'].tolist()
        groupCoLists = []
        currentPerformanceIndicatorCode = 0
        currentCourse = 0

        with connection.cursor() as cursor:
            #Get the greatest idIndicatorGroup
            query='SELECT "idIndicatorGroup" FROM aesci_api_indicatorgroup WHERE "idIndicatorGroup" = (SELECT max("idIndicatorGroup") from aesci_api_indicatorgroup)'
            cursor.execute(query)
            result=cursor.fetchone()

        try:
            currentMaxIndicatorGroup = result[0]
        except:
            currentMaxIndicatorGroup = 0        

        for i in range(len(courseCode)):	
            if pandas.isnull(courseCode[i]) != True:
                try:
                  courseTest = Course.objects.get(codeCourse=courseCode[i])
                except:
                  courseTest, _ = Course.objects.get_or_create(codeCourse=courseCode[i], nameCourse=courseName[i], departmentCourse= [program[i]])                
				#Search for each course its groupCo related rows
				#Beware: you have to change temporarily what's returned in the model of GroupCo to return the idGroupCo
                groupCoLists.append(GroupCo.objects.filter(course=courseCode[i]))
				#Now get the performanceIndicators for this course
                currentCourseIndicators = []
                isTheNextindicatorOfAnotherCourse = False
                for y in range(len(indicatorsCode)):
                    if (isTheNextindicatorOfAnotherCourse == False) and ((currentPerformanceIndicatorCode+1) != len(indicatorsCode)):
                        currentCourseIndicators.append(indicatorsCode[currentPerformanceIndicatorCode])
                        currentPerformanceIndicatorCode += 1
                        if pandas.isnull(courseCode[currentPerformanceIndicatorCode]) != True:
                            isTheNextindicatorOfAnotherCourse = True
                    else:
                        break
				#Now for each groupCo add the correspondent indicatorGroup row if it's not been created yet
				#if there is no group then continue
                #if groupCoLists[i]:
                for x in range(len(groupCoLists[currentCourse])):
                    if not groupCoLists[currentCourse]:
                        print("there is not")
                    else:
                        for z in range(len(currentCourseIndicators)):
                            currentPerformanceIndicator = PerformanceIndicator.objects.get(codePI=currentCourseIndicators[z])
                            currentIndicatorGroup = IndicatorGroup.objects.filter(numGroup=groupCoLists[currentCourse][x], performanceIndicator=currentPerformanceIndicator.idPerformanceIndicator)
                            if not currentIndicatorGroup:
                                currentMaxIndicatorGroup += 1
                                obj, _ = IndicatorGroup.objects.get_or_create(idIndicatorGroup=currentMaxIndicatorGroup, performanceIndicator=currentPerformanceIndicator, numGroup=groupCoLists[currentCourse][x])
                currentCourse += 1

#        # Path to temp file
        tmp_file = os.path.join(settings.MEDIA_ROOT, path)
        os.remove(tmp_file)

        return Response( f'Rubrics, StudentOutcomes, PerformanceIndicators and IndicatorMeasures successfully uploaded' , status=status.HTTP_200_OK)