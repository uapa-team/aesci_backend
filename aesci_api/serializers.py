from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.models import User, Group
from .models import Course, Assignment, IndicatorMeasure, PerformanceIndicator, Rubric, StudentOutcome


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'


class AssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignment
        fields = '__all__'


class RubricSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rubric
        fields = '__all__'


class StudentOutcomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentOutcome
        fields = '__all__'


class PerformanceIndicatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = PerformanceIndicator
        fields = '__all__'


class IndicatorMeasureSerializer(serializers.ModelSerializer):
    class Meta:
        model = IndicatorMeasure
        fields = '__all__'


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
    
        customToken = { 
            'access': str(token.access_token),
            'refresh': str(token),
            'username': user.username,
            'role': user.groups.first().name
        }
    
        return customToken
