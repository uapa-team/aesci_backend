from rest_framework import serializers
from .models import course

class courseSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = course
        fields = '__all__'


