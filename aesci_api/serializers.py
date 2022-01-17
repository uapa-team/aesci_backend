from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.models import User, Group
from .models import * 


class AssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignment
        fields = '__all__'

class AssignmentStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssignmentStudent
        fields = '__all__'

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'

class EvaluationAssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = EvaluationAssignment
        fields = '__all__'

class GroupCoSerializer(serializers.ModelSerializer):
    course = CourseSerializer()
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

class IndicatorMeasureSerializer(serializers.ModelSerializer):
    class Meta:
        model = IndicatorMeasure
        fields = '__all__'

class IndicatorGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = IndicatorGroup
        fields = '__all__'
        
class IndicatorAssignmentSerializer(serializers.ModelSerializer):
    evaluation = EvaluationAssignmentSerializer()
    class Meta:
        model = IndicatorAssignment
        fields = '__all__'

class PerformanceIndicatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = PerformanceIndicator
        fields = '__all__'

class RubricSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rubric
        fields = '__all__'

class StudentOutcomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentOutcome
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
