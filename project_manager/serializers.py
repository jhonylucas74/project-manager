from rest_framework import serializers
from .models import Document, Project, Milestone, Task

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

class PaginatedDocumentSerializer(serializers.Serializer):
    count = serializers.IntegerField()
    next = serializers.URLField(allow_null=True, required=False)
    previous = serializers.URLField(allow_null=True, required=False)
    results = DocumentSerializer(many=True)

class MilestoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Milestone
        fields = '__all__'

class UpdateMilestoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Milestone
        fields = '__all__'
        extra_kwargs = {
            'name': {'required': False},
            'project': {'required': False}
        }

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'

class UpdateTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'
        extra_kwargs = {
            'name': {'required': False},
            'project': {'required': False}
        }

class ProjectSerializer(serializers.ModelSerializer):
    documents = DocumentSerializer(many=True, read_only=True)
    milestones = MilestoneSerializer(many=True, read_only=True)
    tasks = TaskSerializer(many=True, read_only=True)
    

    class Meta:
        model = Project
        fields = '__all__'