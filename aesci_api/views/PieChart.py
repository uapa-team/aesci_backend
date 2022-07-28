from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from django.db import connection

class PieChartView(APIView):
    
	def get(self, request, *args, **kwargs):
		"""
    	Gets the information to create the pie chart. Uses a course, a term and a student Outcome
		and gives an array with the total amount in each measure. 
    	"""
		courseId = self.request.query_params['courseId']
		period = self.request.query_params['period']
		studentOutcome = self.request.query_params['studentOutcome']

		with connection.cursor() as cursor:
            #The query takes information from a course, a period and a student outcome, and returns a table
			#with two columns: the first have the student id and the second all the grades from the student.
			#This table does not have the information regarding the nature of the evaluation, only the grades.
			query=f'''SELECT  seis."idGroupStudent",
	        aesci_api_evaluationAssignment."codeMeasure"
            FROM (aesci_api_evaluationAssignment
	        INNER JOIN (
			SELECT aesci_api_indicatorassignment."idIndicatorAssignment"
			FROM aesci_api_indicatorassignment
            INNER JOIN (
			SELECT aesci_api_indicatorgroup."idIndicatorGroup",
			uno.description
			FROM (aesci_api_indicatorgroup
			INNER JOIN (
			SELECT aesci_api_performanceindicator."idPerformanceIndicator",
			aesci_api_performanceindicator."description"
			FROM aesci_api_performanceindicator
			WHERE aesci_api_performanceindicator."codeSO_id" =  \'{studentOutcome}\'
			)
			AS uno
			ON uno."idPerformanceIndicator" = aesci_api_indicatorgroup."performanceIndicator_id"
			)INNER JOIN (
			SELECT aesci_api_groupco."idGroupCo"
			FROM aesci_api_groupco
			WHERE aesci_api_groupco."periodPlan" = \'{period}\' and aesci_api_groupco.course_id = \'{courseId}\'
			)
		    AS dos
			ON dos."idGroupCo" = aesci_api_indicatorgroup."numGroup_id"
			)
			AS tres
			ON tres."idIndicatorGroup" = aesci_api_indicatorassignment."indicatorGroup_id"
	        )
			AS cuatro
			ON cuatro."idIndicatorAssignment" = aesci_api_evaluationAssignment."indicatorAssignment_id"
            )INNER JOIN (
			SELECT aesci_api_assignmentstudent."idAssignmentStudent",
			cinco."idGroupStudent"
		    FROM aesci_api_assignmentstudent
			INNER JOIN (
			SELECT aesci_api_groupstudent."idGroupStudent"
			FROM aesci_api_groupstudent
			INNER JOIN (
			SELECT aesci_api_groupco."idGroupCo"
			FROM aesci_api_groupco
			WHERE aesci_api_groupco."periodPlan" = \'{period}\' and aesci_api_groupco.course_id = \'{courseId}\'
			)
			AS dos
			ON dos."idGroupCo" = aesci_api_groupstudent."numGroup_id"
			)
			AS cinco
			ON cinco."idGroupStudent" = aesci_api_assignmentstudent."GroupStudent_id"
		 	)
			AS seis
			ON seis."idAssignmentStudent" = aesci_api_evaluationAssignment."assignmentStudent_id"
            order by "idGroupStudent";'''
			cursor.execute(query)
            # Get all rows of query
			query_result = cursor.fetchall()
			res=[0,0,0,0]
			#Append the values -1 to the end of the list to signal the finalization of the data
			query_result.append(('-1','-1'))
			#Create the currentStudent as the first student. This will change as the code iterates the list created by the query
			first=query_result[0]
			currentStudent=first[0]
			#Create the counters
			measureSum=0
			measureCount=0
			studentCount=0

			for element in query_result:
				#If the student in element is the current student, only update the counters
				if element[0]==currentStudent:
					measureSum=measureSum+int(element[1])
					measureCount=measureCount+1
					print(measureCount)
					print(measureSum)
				#Use the counters to calculate the averages of the last student
				#and add to the res list, depending on their value
				elif element[0]!='-1':
					studentCount=studentCount+1
					currentStudent=int(element[0])
					averageMeasure=measureSum/measureCount
					measureSum=int(element[1])
					measureCount=1
					if averageMeasure >= 0 and averageMeasure <= 1:
						res[3]=res[3]+1
					elif averageMeasure > 1 and averageMeasure <= 2:
						res[2]=res[2]+1
					elif averageMeasure > 2 and averageMeasure <= 3:
						res[1]=res[1]+1
					elif averageMeasure > 3 and averageMeasure <= 4:
						res[0]=res[0]+1
				#Otherwise, if the student is -1, this is the end of the list. Calculate the last student's average and update the res list
				else:
					studentCount=studentCount+1
					averageMeasure=measureSum/measureCount
					measureSum=int(element[1])
					measureCount=1
					if averageMeasure >= 0 and averageMeasure <= 1:
						res[3]=res[3]+1
					elif averageMeasure > 1 and averageMeasure <= 2:
						res[2]=res[2]+1
					elif averageMeasure > 2 and averageMeasure <= 3:
						res[1]=res[1]+1
					elif averageMeasure > 3 and averageMeasure <= 4:
						res[0]=res[0]+1
			#Calculate the percentage in each categorie of the res list to create the finalRes list
			finalRes = [0,0,0,0]
			finalCount= 0
			for el in res:
				if studentCount!=0:
					finalRes[finalCount]=(el/studentCount)*100
				finalCount=finalCount+1
			print(finalRes)
		return Response([studentCount,res,finalRes], status=status.HTTP_200_OK)
