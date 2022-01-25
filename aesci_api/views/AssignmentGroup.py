from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from django.db import connection

from ..models import GroupCo, GroupStudent, Student

class AssignmentGroupView(APIView):
    """Create relations between groups and students"""
    
    def get(self, request):
        with connection.cursor() as cursor:
            query = '''SELECT DISTINCT myselect.course_id, "numGroup_id",  myselect.username_id, myselect."periodPlan", aesci_api_assignment."nameAssignment", aesci_api_assignment.description, aesci_api_assignment."idAssignment"
                FROM aesci_api_assignment INNER JOIN
                    (SELECT aesci_api_groupco.id, aesci_api_groupco.course_id, aesci_api_groupco."periodPlan", aesci_api_groupco."numGroup", aesci_api_groupstudent.username_id FROM aesci_api_groupco
                    INNER JOIN aesci_api_groupstudent on aesci_api_groupco.id = aesci_api_groupstudent."numGroup_id" WHERE username_id = '''+ "'" + self.request.query_params["username"]+ "'" +''') AS myselect
                on aesci_api_assignment."numGroup_id" = myselect."id"'''
            cursor.execute(query)
            # Get all rows of query
            query_result = cursor.fetchall()
            res = {}

            # Build dict with assignments group by course
            for element in query_result:
                if res.get(element[0]) is None:
                    res[element[0]] = []
                    aux = {}
                    aux['numGroup'] = element[1]
                    aux['username'] = element[2]
                    aux['period'] = element[3]
                    aux['name'] = element[4]
                    aux['description'] = element[5]
                    aux['idAssignment'] = element[6]
                    res[element[0]].append(aux)
                else:
                    aux = {}
                    aux['numGroup'] = element[1]
                    aux['username'] = element[2]
                    aux['period'] = element[3]
                    aux['name'] = element[4]
                    aux['description'] = element[5]
                    aux['idAssignment'] = element[6]
                    res[element[0]].append(aux)
                    
        return Response( res, status=status.HTTP_200_OK)

