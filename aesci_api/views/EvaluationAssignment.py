from rest_framework import viewsets, permissions, status
from rest_framework.response import Response

from ..models import EvaluationAssignment
from ..serializers import EvaluationAssignmentSerializer

# create evaluation to assignments
class EvaluationAssignmentViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows admin to create evaluation to assignments.
    """
    queryset = EvaluationAssignment.objects.all()
    serializer_class = EvaluationAssignmentSerializer
    permission_classes = [permissions.IsAdminUser]

    def create(self, request):
        isNumber = self.request.query_params["isNumber"]
        grade = self.request.query_params["grade"]

        if isNumber == True:
            if grade < 2.1:
                codeMeasure = "1"
            elif grade < 3.0:
                codeMeasure = "2"
            elif grade < 4.3:
                codeMeasure = "3"
            else:
                codeMeasure = "4"
            EvaluationAssignment.objects.create(qualifier= self.request.query_params["qualifier"], codeMeasure=self.request.query_params["codeMeasure"], grade = grade, evalutionType=self.request.query_params["evaluationType"])
        else:
            EvaluationAssignment.objects.create(qualifier= self.request.query_params["qualifier"], codeMeasure=self.request.query_params["codeMeasure"], evalutionType=self.request.query_params["evaluationType"])

        return Response( status=status.HTTP_200_OK)



