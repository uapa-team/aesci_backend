from unicodedata import numeric
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from django.db import connection

from ..models import GroupCo, PerformanceIndicator, IndicatorGroup, Course, EvaluationAssignment, Student, StudentOutcome

class GetCourseOutcomesView(APIView):
    """Create relations between groups and students"""
    
    def get(self, request):
		#get requested course
        courseId = request.data['course']

		#get course groups
        groups = GroupCo.objects.all().filter(course=courseId)
        #find indicatorgroup rows related to our current groups

        courseStudentOutcomes = []
        for x in groups:
            currentIndicatorGroup = []
            currentPerformanceIndicators = []
            currentStudentOutcomes = []
			#Find indicator groups for each current group
            currentIndicatorGroup = IndicatorGroup.objects.all().filter(numGroup=x.idGroupCo)
			#Find performanceIndicator for each indicatorGroup
            for y in currentIndicatorGroup:
                currentPerformanceIndicators.append(PerformanceIndicator.objects.get(idPerformanceIndicator=y.performanceIndicator.idPerformanceIndicator))
			#Find studentOutcome for each performanceIndicator
            for y in currentPerformanceIndicators:
                currentStudentOutcomes.append([y.codeSO.id, y.codeSO.description])
            courseStudentOutcomes = courseStudentOutcomes + (currentStudentOutcomes)
		#Currently there are probably StudentOutcomes that appear more than once, then
		#we'll look for them, and just let one of them
        i = 0
        for x in courseStudentOutcomes:
            i += 1
            currentPositionsToDelete = []
            for y in range(len(courseStudentOutcomes)-i):
                if courseStudentOutcomes[y+1][0] == x[0]:
                    currentPositionsToDelete.append(y+1)
            deleted = 0
            for y in currentPositionsToDelete:
                del courseStudentOutcomes[y-deleted]
                deleted += 1


        print(courseStudentOutcomes)
		
        return Response(courseStudentOutcomes, status=status.HTTP_200_OK)


