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

from rest_framework.renderers import JSONRenderer

from ..models import IndicatorAssignment, Rubric, StudentOutcome, PerformanceIndicator, IndicatorMeasure, RubricStudentOutcome, Course, GroupCo, IndicatorGroup, IndicatorAssignment
from ..serializers import PerformanceIndicatorSerializer, StudentOutcomeSerializer
# Create your views here.

class IndicatorGroupBySOView(APIView):
    """
    Allows to get the IndicatorGroup objects from a Student Outcome.
    """
    def get(self, pk=None):
        print(self.request.query_params["numgroup"])
        #Check for the purpose of the query
        if self.request.query_params["purpose"] == "create":
            #Check if there are indicators for the group in the request data
            if IndicatorGroup.objects.filter(numGroup=self.request.query_params["numgroup"]).exists():
                IndicatorsGroupByStudentOutcome = [[]]
                #Iterates in all the indicatorGroup objects with the group given in the request
                for x in IndicatorGroup.objects.all().filter(numGroup=self.request.query_params["numgroup"]):
                    #Get the Id of the studentOutcome related to the indicator in the current IndicatorGroup object
                    serializer = StudentOutcomeSerializer(StudentOutcome.objects.get(id = x.performanceIndicator.codeSO.id))
                    #Check if the studentoutcome got from the serializer is in the final list
                    if serializer.data in IndicatorsGroupByStudentOutcome[0]:
                        #Appends the performance indicator in after the last indicator with the same student outcome
                        serializerPI = PerformanceIndicatorSerializer(PerformanceIndicator.objects.get(idPerformanceIndicator = x.performanceIndicator.idPerformanceIndicator))
                        IndicatorsGroupByStudentOutcome[IndicatorsGroupByStudentOutcome[0].index(serializer.data)+1].append(serializerPI.data)
                    else:
                        #Get the student outcome and the performance indicator to append them to the final list
                        serializer = StudentOutcomeSerializer(StudentOutcome.objects.get(id = x.performanceIndicator.codeSO.id))
                        IndicatorsGroupByStudentOutcome[0].append(serializer.data)
                        serializer = PerformanceIndicatorSerializer(PerformanceIndicator.objects.get(idPerformanceIndicator = x.performanceIndicator.idPerformanceIndicator))
                        IndicatorsGroupByStudentOutcome.append([serializer.data])
                return Response(IndicatorsGroupByStudentOutcome, status=status.HTTP_200_OK)
            else:
                return Response("No hay ningún indicator asociado a ese grupo", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        elif self.request.query_params["purpose"] == "update":
            #Check if there are indicators for the group in the request data
            if IndicatorGroup.objects.filter(numGroup=self.request.query_params["numgroup"]).exists():
                IndicatorsGroupByStudentOutcome = [[]]
                #Iterates in all the indicatorGroup objects with the group given in the request
                for x in IndicatorGroup.objects.all().filter(numGroup=self.request.query_params["numgroup"]):
                    #Get the Id of the studentOutcome related to the indicator in the current IndicatorGroup object
                    serializer = StudentOutcomeSerializer(StudentOutcome.objects.get(id = x.performanceIndicator.codeSO.id))
                    #Check if the studentoutcome got from the serializer is in the final list
                    if serializer.data in IndicatorsGroupByStudentOutcome[0]:
                        #Appends the performance indicator in after the last indicator with the same student outcome
                        serializerPI = PerformanceIndicatorSerializer(PerformanceIndicator.objects.get(idPerformanceIndicator = x.performanceIndicator.idPerformanceIndicator))
                        #Checks if the object exists to update it
                        if IndicatorAssignment.objects.filter(indicatorGroup=x.idIndicatorGroup, assignment=self.request.query_params["assignment"]).exists():
                            IndicatorsGroupByStudentOutcome[IndicatorsGroupByStudentOutcome[0].index(serializer.data)+1].append([serializerPI.data,"True"])
                        else:
                            IndicatorsGroupByStudentOutcome[IndicatorsGroupByStudentOutcome[0].index(serializer.data)+1].append([serializerPI.data,"False"])
                    else:
                        #Get the student outcome and the performance indicator to append them to the final list
                        serializer = StudentOutcomeSerializer(StudentOutcome.objects.get(id = x.performanceIndicator.codeSO.id))
                        IndicatorsGroupByStudentOutcome[0].append(serializer.data)
                        serializer = PerformanceIndicatorSerializer(PerformanceIndicator.objects.get(idPerformanceIndicator = x.performanceIndicator.idPerformanceIndicator))
                        if IndicatorAssignment.objects.filter(indicatorGroup=x.idIndicatorGroup, assignment=self.request.query_params["assignment"]).exists():
                            IndicatorsGroupByStudentOutcome.append([[serializer.data,"True"]])
                        else:
                            IndicatorsGroupByStudentOutcome.append([[serializer.data,"False"]])
                return Response(IndicatorsGroupByStudentOutcome, status=status.HTTP_200_OK)
            else:
                return Response("No hay ningún indicator asociado a ese grupo", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response("Porfavor ingrese un valor adecuado para la variable 'purpose' ", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
