from rest_framework import viewsets, permissions, status
from rest_framework.response import Response

from ..models import EvaluationAssignment, IndicatorAssignment
from ..serializers import EvaluationAssignmentSerializer
from ..helpers import EVTYPES

# create evaluation to assignments
class EvaluationAssignmentViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows admin to create evaluation to assignments.
    """
    queryset = EvaluationAssignment.objects.all()
    serializer_class = EvaluationAssignmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request):
        isNumber = self.request.query_params["isNumber"]
        grade = self.request.data["grade"]
        indicatorAssignment = IndicatorAssignment.objects.get(id = self.request.data["indicatorAssignment"])    
        evaluationType = self.request.data["evaluationType"]
        qualifier = self.request.data["qualifier"]

        if isNumber == "True":
            if float(grade) < 2.1:
                codeMeasure = "1"
            elif float(grade) < 3.0:
                codeMeasure = "2"
            elif float(grade) < 4.3:
                codeMeasure = "3"
            else:
                codeMeasure = "4"

            EvaluationAssignment.objects.create(qualifier= qualifier, codeMeasure=codeMeasure, grade=grade, indicatorAssignment=indicatorAssignment, evaluationType=evaluationType)
        else:
            EvaluationAssignment.objects.create(qualifier= qualifier, codeMeasure=self.request.data["codeMeasure"], indicatorAssignment=indicatorAssignment, evaluationType=evaluationType)

        return Response( status=status.HTTP_200_OK)



