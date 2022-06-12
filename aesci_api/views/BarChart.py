from unicodedata import numeric
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from django.db import connection

from ..models import GroupCo, PerformanceIndicator, IndicatorGroup, IndicatorAssignment, EvaluationAssignment

class BarChartView(APIView):
    """Create relations between groups and students"""
    
    def get(self, request):
        studentOutcomeId = self.request.query_params['studentOutcome']
        semester = self.request.query_params['semester']
        courseId = self.request.query_params['course']
		#Get all performanceIndicator objects of selected studentOutcome
        performanceIndicators = PerformanceIndicator.objects.all().filter(codeSO=studentOutcomeId)
		#get all groups of the requested course in the requested semester
        groups = GroupCo.objects.all().filter(course=courseId,periodPlan=semester)

        indicatorsGroupList = []
		#get indicatorGroup objects that have one performance indicator in our performanceIndicators list
		#and one group of our groups list
        for x in performanceIndicators:
            currentIndicatorGroups = []
            for y in groups:
                if IndicatorGroup.objects.filter(performanceIndicator=x.idPerformanceIndicator,numGroup=y.idGroupCo).exists():
                    currentIndicatorGroups.append(IndicatorGroup.objects.get(performanceIndicator=x.idPerformanceIndicator,numGroup=y.idGroupCo))
			#We append an array with the performanceIndicator and the indicatorGroups of that performanceIndicator
            indicatorsGroupList.append([x,currentIndicatorGroups])

        indicatorAssignmentsList = []
		#Now get indicatorAssignment object that have a fk of one of our indicatorGroups
        for x in indicatorsGroupList:
			#X is the list of indicatorsGroup of first found of performanceIndicator
            currentIndicatorAssignments = []
            for y in x[1]:
				#Y is a single indicatorGroup of a performanceIndicator
                if IndicatorAssignment.objects.filter(indicatorGroup=y.idIndicatorGroup).exists():
                    currentIndicatorAssignments.append(IndicatorAssignment.objects.all().filter(indicatorGroup=y.idIndicatorGroup))            
			#We append an array with the performanceIndicator and the indictorAssignments of that performanceIndicator
            indicatorAssignmentsList.append([x[0],currentIndicatorAssignments])

		#Get the grades of the assignments related with the performanceIndicators we have
        indicatorGradesList = []
        for x in indicatorAssignmentsList:
			#Get grades of assignments related to current performanceIndicator
            currentIndicatorGrades = []
            for y in x[1]:
                for z in y:
                    if EvaluationAssignment.objects.filter(indicatorAssignment=z.idIndicatorAssignment).exists():
                        currentIndicatorGrades.append(EvaluationAssignment.objects.filter(indicatorAssignment=z.idIndicatorAssignment))            
			#We append an array with the performanceIndicator and the grades of assignments of that performanceIndicator
            indicatorGradesList.append([x[0],currentIndicatorGrades])

		#Now that we got the grades of indicators let's calculate the percentages
        indicatorPercentagesList = []
        for x in indicatorGradesList:     
			#Each indicator has 4 percentages corresponding to the 4 possible indicators       
            currentIndicatorPercentages = [0,0,0,0]
            numberEvaluations = 0
            for y in x[1]:
				#save the number of grades of assignments related with current performanceIndicator
                numberEvaluations = y.count()
                for z in y:
					#We'll add 1 to the index of the measure of current assignment 
                    currentIndicatorPercentages[(int(z.codeMeasure))-1]=currentIndicatorPercentages[(int(z.codeMeasure))-1]+1
			#Sometimes, indicators don't have yet any assignment, so that numberEvaluations=0 then the percentage we'll be 0 as
			#we've defined initially in the array
			#If there is any assignment related with the performance indicator that has been grade then
			#numberEvaluations!=0
            if numberEvaluations!=0 :
                currentIndicatorPercentages = [w/numberEvaluations for w in currentIndicatorPercentages]
			#Now add the id of the performanceIndicator along with its correspondant percentages
            indicatorPercentagesList.append([x[0].idPerformanceIndicator, currentIndicatorPercentages])

        return Response(indicatorPercentagesList, status=status.HTTP_200_OK)


