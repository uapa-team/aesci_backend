from rest_framework import serializers
from .models import Course

class CourseSerializer(serializers.ModelSerializer):
    codeCourse = serializers.IntegerField()
    periodPlan = serializers.CharField()
    referencePlan = serializers.IntegerField()
    nameCourse = serializers.CharField()
    departmentCourse = serializers.CharField()

    class Meta:
            model = Course
            fields = '__all__'

    def createCourse(self, validated_data):
        """
        Create and return a new `Course` instance, given the validated data.
        """
        return Course.objects.create(**validated_data)

