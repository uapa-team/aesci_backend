from rest_framework import viewsets, permissions

from .models import course
from .serializers import courseSerializer

# Create your views here.
class courseViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = course.objects.all()
    serializer_class = courseSerializer
    # permissions = [permissions.IsAuthenticated]
