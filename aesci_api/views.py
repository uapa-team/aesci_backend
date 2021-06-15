from django.shortcuts import render
from .models import Course
from rest_framework import viewsets,permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import CourseSerializer

# Create your views here.
class CourseViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    # permissions = [permissions.IsAuthenticated]

    @api_view(['GET', 'POST'])
    def hello_world(request):
        if request.method == 'POST':
            return Response({"message": "Got some data!", "data": request.data})
        return Response({"message": "Hello, world!"})