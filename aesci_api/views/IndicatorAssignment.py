from rest_framework import viewsets, permissions, status
from rest_framework.response import Response

from ..models import IndicatorAssignment, IndicatorGroup
from ..serializers import IndicatorAssignmentSerializer

# create indicator assignment
class IndicatorAssignmentViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows admin to create indicator assignment.
    """
    serializer_class = IndicatorAssignmentSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self, pk=None):
        if IndicatorAssignment.objects.filter(assignment=self.request.query_params["assignment"]).exists():
            return IndicatorAssignment.objects.filter(assignment=self.request.query_params["assignment"])
        else:
            return None 

    def create(self, request):
        indicators = request.data["indicators"]
        assignment = request.data["assignment"]

        # data validated 
        data = []

        # Search and store valid indicators
        for indicator in indicators:
            try:
                validatedIndicator = IndicatorGroup.objects.get( idIndicatorGroup = indicator)
            except:
                continue

            data.append(validatedIndicator.idIndicatorGroup)

        # Save indicators for each assignment
        for indicator in data:  
            IndicatorAssignment.objects.create(assignment_id = assignment, indicatorGroup_id = indicator)

        return Response( status=status.HTTP_200_OK)