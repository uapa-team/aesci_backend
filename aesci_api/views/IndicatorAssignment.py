from rest_framework import viewsets, permissions, status
from rest_framework.response import Response

from ..models import IndicatorAssignment, IndicatorGroup
from ..serializers import IndicatorAssignmentSerializer

# create indicator assignment
class IndicatorAssignmentViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows admin to create indicator assignment.
    """
    queryset = IndicatorAssignment.objects.all()
    serializer_class = IndicatorAssignmentSerializer
    permission_classes = [permissions.AllowAny]


    def create(self, request):
        indicators = request.data["indicators"]
        homework = request.data["homework"]

        # data validated 
        data = []

        # Search and store valid indicators
        for indicator in indicators:
            try:
                validatedIndicator = IndicatorGroup.objects.get( id = indicator)
            except:
                continue

            data.append(validatedIndicator.id)

        # Save indicators for each homework
        for indicator in data:  
            IndicatorAssignment.objects.create(homework_id = homework, indicatorGroup_id = indicator)

        return Response( status=status.HTTP_200_OK)