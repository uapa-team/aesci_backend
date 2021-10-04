from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.models import User, Group
from .models import Course, Assignment, GroupCo, GroupStudent, GroupTeacher


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'


class AssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignment
        fields = '__all__'

class GroupCoSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupCo
        fields = '__all__'

class GroupStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupStudent
        fields = '__all__'

class GroupTeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupTeacher
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
