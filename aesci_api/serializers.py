from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.models import User, Group
from .models import * 



class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'
        
class GroupCoSerializer(serializers.ModelSerializer):
    course = CourseSerializer()
    class Meta:
        model = GroupCo
        fields = '__all__'

class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = '__all__'

class AssignmentSerializer(serializers.ModelSerializer):
    username = TeacherSerializer()
    numGroup = GroupCoSerializer()
    class Meta:
        model = Assignment
        fields = '__all__'

class AssignmentStudentSerializer(serializers.ModelSerializer):
    Assignment = AssignmentSerializer()
    class Meta:
        model = AssignmentStudent
        fields = '__all__'


class EvaluationAssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = EvaluationAssignment
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

class PerformanceIndicatorSerializer(serializers.ModelSerializer):
    # measures = IndicatorMeasureSerializer(many=True)    
    class Meta:
        model = PerformanceIndicator
        fields = ['id','codePI','description','codeSO']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        levels = IndicatorMeasure.objects.filter(performanceIndicator=instance.id)
        arr_levels = levels.values_list()
        final_levels = []

        # Get dict from indicators' measure 
        for element in arr_levels:
            level_element = {'id':element[0],
                'codeMeasure':element[1],
                'description':element[2],
                'performanceIndicator':element[3]
            }
            final_levels.append(level_element)
        
        # Add array of measures to response
        representation['levels'] = final_levels 
        return representation

class IndicatorGroupSerializer(serializers.ModelSerializer):
    performanceIndicator = PerformanceIndicatorSerializer()
    class Meta:
        model = IndicatorGroup
        fields = '__all__'
        
class IndicatorAssignmentSerializer(serializers.ModelSerializer):
    # assignment = AssignmentSerializer()
    indicatorGroup = IndicatorGroupSerializer()
    class Meta:
        model = IndicatorAssignment
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
