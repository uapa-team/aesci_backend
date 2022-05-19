from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from django.db import connection

from ..models import Rubric, StudentOutcome, RubricStudentOutcome

class GetRubricStudentOutcomeView(APIView):
    """Create relations between groups and students"""
    
    def get(self, request):

        #To do later
        #with connection.cursor() as cursor:
        #    query = ''
        #    cursor.execute(query)
        #    # Get all rows of query
        #    query_result = cursor.fetchall()
        #    res = {}
#
        #    # Build dict with assignments group by course
        #    for element in query_result:
        #        
        #    
        #    res = list(res.items())

        return Response( res, status=status.HTTP_200_OK)


