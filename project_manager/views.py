from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import generics, pagination
from rest_framework import status
from .serializers import FileSerializer, DocumentSerializer, ProjectSerializer, PaginatedDocumentSerializer, DocumentDetailSerializer
from .models import Document, Project
from django.conf import settings
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated

class DocumentUploadListView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)

    @swagger_auto_schema(
        request_body=FileSerializer,
        responses={
            status.HTTP_201_CREATED: DocumentSerializer,
            status.HTTP_400_BAD_REQUEST: 'Bad Request',
            status.HTTP_404_NOT_FOUND: 'Project not found'
        }
    )
    def post(self, request, *args, **kwargs):
        serializer = FileSerializer(data=request.data)

        if serializer.is_valid():
            file = serializer.validated_data['file']
            project_id = serializer.validated_data['project_id']

            try:
                project = Project.objects.get(pk=project_id)
            except Project.DoesNotExist:
                return Response({ 'status': 'Project not found' }, status=status.HTTP_404_NOT_FOUND)

            doc = Document.objects.create(
                name=file.name,
                extension=file.name.split('.')[-1],
                file=file
            )

            project.documents.add(doc)

            data = DocumentSerializer(doc).data
            return Response({ 'status': 'File sent with success', 'data': data }, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: PaginatedDocumentSerializer
        }
    )
    def get(self, request, *args, **kwargs):
        paginator = pagination.PageNumberPagination()
        paginator.page_size = settings.PAGE_SIZE 

        documents = Document.objects.all()
        result_page = paginator.paginate_queryset(documents, request)
        serializer = DocumentSerializer(result_page, many=True)

        return paginator.get_paginated_response(serializer.data)

class DocumentRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Document.objects.all()
    serializer_class = DocumentDetailSerializer
    permission_classes = [IsAuthenticated]

class ProjectListCreateAPIView(generics.ListCreateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    pagination_class = pagination.PageNumberPagination
    pagination_class.page_size = settings.PAGE_SIZE
    permission_classes = [IsAuthenticated]

class ProjectRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]
