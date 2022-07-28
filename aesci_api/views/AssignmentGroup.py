from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from django.db import connection

from ..models import GroupCo, GroupStudent, Student, Assignment, AssignmentStudent, EvaluationAssignment


class AssignmentGroupView(APIView):
    """
    Retrieve the information of all the assignments from the groups a student is in
    """
    
    def get(self, request):
        with connection.cursor() as cursor:
            # The query searches for the group a certain student is in,
            # and then gets all the information of the assignments from
            # this group
            query = '''SELECT DISTINCT myselect.course_id, "numGroup_id",  myselect.username_id, myselect."periodPlan", aesci_api_assignment."nameAssignment", aesci_api_assignment.description, aesci_api_assignment."idAssignment"
                FROM aesci_api_assignment INNER JOIN
                    (SELECT aesci_api_groupco."idGroupCo", aesci_api_groupco."course_id", aesci_api_groupco."periodPlan", aesci_api_groupco."numGroup", aesci_api_groupstudent.username_id FROM aesci_api_groupco
                    INNER JOIN aesci_api_groupstudent on aesci_api_groupco."idGroupCo" = aesci_api_groupstudent."numGroup_id" WHERE username_id = ''' + "'" + self.request.query_params["username"] + "'" + ''') AS myselect
                on aesci_api_assignment."numGroup_id" = myselect."idGroupCo"'''
            cursor.execute(query)
            # Get all rows of query
            query_result = cursor.fetchall()
            res = {}

            # Build dict with assignments group by course
            for element in query_result:
                cursor.execute(
                    f'SELECT "nameCourse" FROM aesci_api_course WHERE "codeCourse" = \'{element[0]}\' ')
                result = cursor.fetchone()
                print(result[0])
                if res.get(result[0]) is None:
                    res[result[0]] = []
                    aux = {}
                    aux['numGroup'] = element[1]
                    aux['username'] = element[2]
                    aux['period'] = element[3]
                    aux['name'] = element[4]
                    aux['description'] = element[5]
                    aux['idAssignment'] = element[6]
                    assignmentObject = Assignment.objects.get(
                        idAssignment=element[6])
                    assignmentObject.link
                    aux['assignmentLinks'] = assignmentObject.link
                    # Now, let's see if this assignment of this student was already evaluated by looking
                    # for any evaluatioon for the assignmentStudent object related
                    groupStudent = GroupStudent.objects.get(
                        username=element[2], numGroup=element[1])
                    assignmentStudent = AssignmentStudent.objects.get(
                        GroupStudent=groupStudent.idGroupStudent, Assignment=element[6])
                    if EvaluationAssignment.objects.filter(assignmentStudent=assignmentStudent.idAssignmentStudent).exists():
                        aux['evaluated'] = "True"
                    else:
                        aux['evaluated'] = "False"
                    res[result[0]].append(aux)
                else:
                    aux = {}
                    aux['numGroup'] = element[1]
                    aux['username'] = element[2]
                    aux['period'] = element[3]
                    aux['name'] = element[4]
                    aux['description'] = element[5]
                    aux['idAssignment'] = element[6]
                    assignmentObject = Assignment.objects.get(
                        idAssignment=element[6])
                    assignmentObject.link
                    aux['assignmentLinks'] = assignmentObject.link
                    # Now, let's see if this assignment of this student was already evaluated by looking
                    # for any evaluatioon for the assignmentStudent object related
                    groupStudent = GroupStudent.objects.get(
                        username=element[2], numGroup=element[1])
                    assignmentStudent = AssignmentStudent.objects.get(
                        GroupStudent=groupStudent.idGroupStudent, Assignment=element[6])
                    if EvaluationAssignment.objects.filter(assignmentStudent=assignmentStudent.idAssignmentStudent).exists():
                        aux['evaluated'] = "True"
                    else:
                        aux['evaluated'] = "False"
                    res[result[0]].append(aux)

            res = list(res.items())

        return Response(res, status=status.HTTP_200_OK)
