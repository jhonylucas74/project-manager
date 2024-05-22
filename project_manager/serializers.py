from rest_framework import serializers
from .models import Document, Project

class FileSerializer(serializers.Serializer):
    project_id = serializers.IntegerField()
    file = serializers.FileField()

class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = '__all__'

class ProjectSerializer(serializers.ModelSerializer):
    documents = DocumentSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = '__all__'
