from rest_framework import viewsets, permissions, status
from rest_framework.response import Response

from ..models import IndicatorGroup, PerformanceIndicator
from ..serializers import IndicatorGroupSerializer

# create indicator group
class IndicatorGroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows admin to create indicator group.
    """
    serializer_class = IndicatorGroupSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self, pk=None):
        if IndicatorGroup.objects.filter(numGroup=self.request.query_params["numgroup"]).exists():
            # Return assignments related to Teacher
            return IndicatorGroup.objects.all().filter(numGroup=self.request.query_params["numgroup"])
        else:
            return None

    def create(self, request):
        indicators = request.data["performanceIndicator"]
        numGroup = request.data["numGroup"]

        # data validated 
        data = []

        # Search and store valid indicators
        for indicator in indicators:
            try:
                validatedIndicator = PerformanceIndicator.objects.get( idPerformanceIndicator = indicator)
            except:
                continue

            data.append(validatedIndicator.idPerformanceIndicator)

        for group in numGroup:
            # Save indicators for each group
            for indicator in data:  
                IndicatorGroup.objects.create(numGroup_id = group, performanceIndicator_id = indicator)

        return Response( status=status.HTTP_200_OK)