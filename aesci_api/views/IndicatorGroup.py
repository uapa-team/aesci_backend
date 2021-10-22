from rest_framework import viewsets, permissions, status
from rest_framework.response import Response

from ..models import IndicatorGroup, PerformanceIndicator
from ..serializers import IndicatorGroupSerializer

# create indicator group
class IndicatorGroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows admin to create indicator group.
    """
    queryset = IndicatorGroup.objects.all()
    serializer_class = IndicatorGroupSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request):
        indicators = request.data["indicators"]
        numGroup = request.data["numGroup"]

        # data validated 
        data = []

        # Search and store valid indicators
        for indicator in indicators:
            try:
                validatedIndicator = PerformanceIndicator.objects.get( id = indicator)
            except:
                continue

            data.append(validatedIndicator.id)

        # Save indicators for each group
        for indicator in data:  
            IndicatorGroup.objects.create(numGroup_id = numGroup, performanceIndicator_id = indicator)

        return Response( status=status.HTTP_200_OK)