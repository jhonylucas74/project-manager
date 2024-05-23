from rest_framework import serializers
from .models import Document, Project

class FileSerializer(serializers.Serializer):
    project_id = serializers.IntegerField()
    file = serializers.FileField()

class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = '__all__'

class DocumentDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = '__all__'
        extra_kwargs = {
            'file': {'required': False}
        }

class ProjectSerializer(serializers.ModelSerializer):
    documents = DocumentSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = '__all__'

class PaginatedDocumentSerializer(serializers.Serializer):
    count = serializers.IntegerField()
    next = serializers.URLField(allow_null=True, required=False)
    previous = serializers.URLField(allow_null=True, required=False)
    results = DocumentSerializer(many=True)