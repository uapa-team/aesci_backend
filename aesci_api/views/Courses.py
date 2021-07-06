from rest_framework import viewsets, permissions

from ..models import Course
from ..serializers import CourseSerializer


class CourseViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [permissions.IsAdminUser]
