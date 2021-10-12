from rest_framework import viewsets, permissions

from ..models import Rubric
from ..serializers import RubricSerializer


class RubricViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows admin to create rubrics.
    """
    queryset = Rubric.objects.all()
    serializer_class = RubricSerializer
    permission_classes = [permissions.IsAdminUser]