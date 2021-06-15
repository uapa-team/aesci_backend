from django.shortcuts import render
from .models import Course
from rest_framework import viewsets,permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import CourseSerializer

# Create your views here.
