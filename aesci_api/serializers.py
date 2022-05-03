from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.models import User, Group
from .models import * 



class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'
        
class GroupCoSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupCo
        fields = '__all__'

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response["course"] = CourseSerializer(instance.course).data
        return response

class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = '__all__'

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'

class AssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignment
        fields = '__all__'

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response["usernameTeacher"] = TeacherSerializer(instance.usernameTeacher).data
        response["numGroup"] = GroupCoSerializer(instance.numGroup).data
        return response

class AssignmentStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssignmentStudent
        fields = '__all__'

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response["Assignment"] = AssignmentSerializer(instance.Assignment).data
        response["GroupStudent"] = GroupStudentSerializer(instance.GroupStudent).data
        return response


class EvaluationAssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = EvaluationAssignment
        fields = '__all__'

class GroupStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupStudent
        fields = '__all__'

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response["username"] = StudentSerializer(instance.username).data
        return response

class GroupTeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupTeacher
        fields = '__all__'

class IndicatorMeasureSerializer(serializers.ModelSerializer):
    class Meta:
        model = IndicatorMeasure
        fields = '__all__'

class PerformanceIndicatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = PerformanceIndicator
        fields = ['idPerformanceIndicator','codePI','description','codeSO', "isActive"]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        levels = IndicatorMeasure.objects.filter(performanceIndicator=instance.idPerformanceIndicator)
        arr_levels = levels.values_list()
        final_levels = []

        # Get dict from indicators' measure 
        for element in arr_levels:
            level_element = {'idIndicatorMeasure':element[0],
                'codeMeasure':element[1],
                'performanceIndicator':element[3],
                'description':element[2]
            }
            final_levels.append(level_element)
        
        # Add array of measures to response
        representation['levels'] = final_levels 
        return representation

class IndicatorGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = IndicatorGroup
        fields = '__all__'

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response["performanceIndicator"] = PerformanceIndicatorSerializer(instance.performanceIndicator).data
        return response


class IndicatorAssignmentSerializer(serializers.ModelSerializer):
    # assignment = AssignmentSerializer()
    class Meta:
        model = IndicatorAssignment
        fields = '__all__'

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response["indicatorGroup"] = IndicatorGroupSerializer(instance.indicatorGroup).data
        response["assignment"] = AssignmentSerializer(instance.assignment).data
        return response


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
