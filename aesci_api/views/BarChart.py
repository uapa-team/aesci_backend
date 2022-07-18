from ast import Assign
from unicodedata import numeric
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from django.db import connection

from ..models import GroupCo, PerformanceIndicator, IndicatorGroup, IndicatorAssignment, EvaluationAssignment, Assignment, AssignmentStudent, GroupStudent, Student

class BarChartView(APIView):
    """Create relations between groups and students"""
    
    def get(self, request):
        studentOutcomeId = self.request.query_params['studentOutcome']
        courseId = self.request.query_params['course']
        semesters =''.join(self.request.query_params["semesters"])
        semesters = semesters.replace('[','')
        semesters = semesters.replace(']','')
        semesters = semesters.replace('"','')
        semesters = semesters.replace(' ','')
        semesters = list(semesters.split(","))

        if(len(semesters) == 1):
            semester = semesters[0]
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
                currentIndicatorStudents = [0,0,0,0]
                numberEvaluations = 0
                for y in x[1]:
    				#save the number of grades of assignments related with current performanceIndicator
                    numberEvaluations = y.count()
                    for z in y:
    					#We'll add 1 to the index of the measure of current assignment 
                        currentIndicatorPercentages[(int(z.codeMeasure))-1]=currentIndicatorPercentages[(int(z.codeMeasure))-1]+1
                        currentIndicatorStudents[(int(z.codeMeasure))-1]=currentIndicatorStudents[(int(z.codeMeasure))-1]+1
    			#Sometimes, indicators don't have yet any assignment, so that numberEvaluations=0 then the percentage we'll be 0 as
    			#we've defined initially in the array
    			#If there is any assignment related with the performance indicator that has been grade then
    			#numberEvaluations!=0
                if numberEvaluations!=0 :
                    currentIndicatorPercentages = [w/numberEvaluations for w in currentIndicatorPercentages]
    			#Now add the id of the performanceIndicator along with its correspondant percentages
                indicatorPercentagesList.append([x[0].idPerformanceIndicator, currentIndicatorPercentages, currentIndicatorStudents])
            return Response(indicatorPercentagesList, status=status.HTTP_200_OK)
        else:
            semestersStatistics = []
            for w in semesters:
                semester = w
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
                    currentIndicatorAssignments = []
                    for y in x[1]:
                        for z in y:
                            if EvaluationAssignment.objects.filter(indicatorAssignment=z.idIndicatorAssignment).exists():
                                currentIndicatorGrades.append(EvaluationAssignment.objects.filter(indicatorAssignment=z.idIndicatorAssignment))
                                currentIndicatorAssignments.append(z.assignment.idAssignment)
        			#We append an array with the performanceIndicator and the grades of assignments of that performanceIndicator
                    indicatorGradesList.append([x[0],currentIndicatorGrades])        

				#In the next array we'll save the grades per student, performande indicator and assignment
                gradesSPA = []
                for x in indicatorGradesList:
                    for y in x[1]:
                        for z in y:
                            assignment = z.assignmentStudent.Assignment.idAssignment
                            groupStudent = GroupStudent.objects.get(idGroupStudent=z.assignmentStudent.GroupStudent.idGroupStudent)
                            student = Student.objects.get(username=groupStudent.username)
                            wasTheTupleStudentAssignmentAlreadyFound = False
                            positionFound = 0
                            for x in gradesSPA:
                                if [student.username,assignment] == x[0]:
                                    wasTheTupleStudentAssignmentAlreadyFound = True
                                    break
                                positionFound += 1
                            if wasTheTupleStudentAssignmentAlreadyFound == True:
                                gradesSPA[positionFound].append(z.codeMeasure) 
                            else:
                                gradesSPA.append([[student.username,assignment],z.codeMeasure])
        		#Now, let's calculate the level of each student in their respective assignments
                percentages = [0,0,0,0]
                students = [0,0,0,0]
                numberEvaluations = 0
                print(gradesSPA)
                for x in gradesSPA:     
                    sum = 0
                    for y in range(len(x)-1):
        				#sum the results obtained in all performance indicator of current student in current assignment
						#remember the tuple that tell us in which student and assignment we're currently at is x[0]
                        sum += int(x[y+1])
                    averageGrade = round(sum/(len(x)-1))
        				#We'll add 1 to the index of the level of current student
                    percentages[averageGrade-1]=percentages[averageGrade-1]+1
                    students[averageGrade-1]=students[averageGrade-1]+1
                if len(gradesSPA)!=0 :
                    percentages = [w/len(gradesSPA) for w in percentages]
                semestersStatistics.append([w, percentages, students])
            return Response(semestersStatistics, status=status.HTTP_200_OK)


