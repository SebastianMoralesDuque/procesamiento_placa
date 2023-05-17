from rest_framework import serializers
from .models import Task

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        # fields = ('id', 'texto_generado:', 'texto_ingresado:', 'precision:')
        fields = '__all__'