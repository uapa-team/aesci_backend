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


from ..models import Rubric, StudentOutcome, PerformanceIndicator, IndicatorMeasure
# Create your views here.

class UploadRubricsView(APIView):
    """Create student's users"""
    def post(self, request, *args, **kwargs):
        file = request.FILES['file']
        print("hola rubrics")
        path = default_storage.save("tmp", ContentFile(file.read()))
        
        data_frame_rubricsInfo = pandas.read_excel(path, sheet_name='Rubrica')

#       # Filter columns we need and then turn them into lists
        rubricsCode = data_frame_rubricsInfo['RubricCode'].tolist()
        rubricsDescription = data_frame_rubricsInfo['RubricName'].tolist()
        studentOutcomesDescription = data_frame_rubricsInfo['StudentOutcome'].tolist()
        PerformanceIndicatorsCode = data_frame_rubricsInfo['PerformanceIndicatorCode'].tolist()
        PerformanceIndicatorsDescription = data_frame_rubricsInfo['PerformanceIndicatorDescription'].tolist()
        IndicatorMeasuresDescription = data_frame_rubricsInfo['IndicatorMeasureDescription'].tolist()		

        with connection.cursor() as cursor:
            #Get the greatest idAssignment to assign the next number to new assignment
            query='SELECT "idRubric" FROM aesci_api_rubric WHERE "idRubric" = (SELECT max("idRubric") from aesci_api_rubric)'
            cursor.execute(query)
            result=cursor.fetchone()

        greatestRubricId = result[0]	
        createdRubricsCounter = 0
        createdRubricsInfo = []
        for i in range(len(rubricsCode)):	
            if pandas.isnull(rubricsCode[i]) != True:
                createdRubricsCounter += 1						
                obj, _ = Rubric.objects.get_or_create(idRubric=greatestRubricId + (createdRubricsCounter), codeRubric=rubricsCode[i], description=rubricsDescription[i],isActive='True',departmentRubric=['2549'])
                createdRubricsInfo.append((greatestRubricId + createdRubricsCounter))

        with connection.cursor() as cursor:
            #Get the greatest idAssignment to assign the next number to new assignment
            query='SELECT "idStudentOutcome" FROM aesci_api_studentoutcome WHERE "idStudentOutcome" = (SELECT max("idStudentOutcome") from aesci_api_studentoutcome)'
            cursor.execute(query)
            result=cursor.fetchone()

        currentRubric = 0
        greatestStudentOutcomeId = result[0]
        createdStudentOutcomesCounter = 0
        createdStudentOutcomeInfo = []
        for i in range(len(studentOutcomesDescription)):			
            if pandas.isnull(studentOutcomesDescription[i]) != True:
                createdStudentOutcomesCounter += 1
                if pandas.isnull(rubricsCode[i]) != True:
                    currentRubric += 1
                    #create the weak entity 
                #now student outcome won't take the id of the rubric but of the weak entity
                currentRubricObject = Rubric.objects.get(idRubric=createdRubricsInfo[currentRubric-1])
                obj, _ = StudentOutcome.objects.get_or_create(idStudentOutcome=greatestStudentOutcomeId + (createdStudentOutcomesCounter), codeRubric=currentRubricObject, isActive='True', description=studentOutcomesDescription[i])
                createdStudentOutcomeInfo.append((greatestStudentOutcomeId + createdStudentOutcomesCounter))
            else:
                if pandas.isnull(rubricsCode[i]) != True:
                    currentRubric += 1
                    #create week entity using current rubric and current studentOutcome
	

        with connection.cursor() as cursor:
            #Get the greatest idAssignment to assign the next number to new assignment
            query='SELECT "idPerformanceIndicator" FROM aesci_api_performanceindicator WHERE "idPerformanceIndicator" = (SELECT max("idPerformanceIndicator") from aesci_api_performanceindicator)'
            cursor.execute(query)
            result=cursor.fetchone()

        currentStudentOutcome = 0
        greatestPerformanceIndicatorId = result[0]
        createdPerformanceIndicatorsCounter = 0
        createdPerformanceIndicatorInfo = []
        for i in range(len(PerformanceIndicatorsCode)):			
            if pandas.isnull(PerformanceIndicatorsCode[i]) != True:
                createdPerformanceIndicatorsCounter += 1
                if pandas.isnull(studentOutcomesDescription[i]) != True:
                    currentStudentOutcome += 1
                currentStudentOutcomeObject = StudentOutcome.objects.get(idStudentOutcome=createdStudentOutcomeInfo[currentStudentOutcome-1])
                obj, _ = PerformanceIndicator.objects.get_or_create(idPerformanceIndicator=greatestPerformanceIndicatorId + (createdPerformanceIndicatorsCounter), codeSO=currentStudentOutcomeObject, codePI= PerformanceIndicatorsCode[i], description=PerformanceIndicatorsDescription[i], isActive='True')
                createdPerformanceIndicatorInfo.append((greatestPerformanceIndicatorId + createdPerformanceIndicatorsCounter))

        with connection.cursor() as cursor:
            #Get the greatest idAssignment to assign the next number to new assignment
            query='SELECT "idIndicatorMeasure" FROM aesci_api_indicatormeasure WHERE "idIndicatorMeasure" = (SELECT max("idIndicatorMeasure") from aesci_api_indicatormeasure)'
            cursor.execute(query)
            result=cursor.fetchone()

        currentPerformanceIndicator = 0
        greatestIndicatorMeasureId = result[0]
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

#        # Path to temp file
        tmp_file = os.path.join(settings.MEDIA_ROOT, path)
        os.remove(tmp_file)

        return Response( f'Rubrics, StudentOutcomes, PerformanceIndicators and IndicatorMeasures successfully uploaded' , status=status.HTTP_200_OK)