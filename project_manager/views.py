from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import generics, pagination
from rest_framework import status
from .serializers import FileSerializer, DocumentSerializer, ProjectSerializer, PaginatedDocumentSerializer, DocumentDetailSerializer
from .models import Document, Project, Status
from django.conf import settings
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated
from .permissions import ProjectPermission, DocumentPermission
from datetime import datetime
from drf_yasg import openapi

class DocumentUploadListView(APIView):
    permission_classes = [IsAuthenticated, DocumentPermission]
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
        documents = documents.order_by('-created_at')
        result_page = paginator.paginate_queryset(documents, request)
        serializer = DocumentSerializer(result_page, many=True)

        return paginator.get_paginated_response(serializer.data)

class DocumentRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Document.objects.all()
    serializer_class = DocumentDetailSerializer
    permission_classes = [IsAuthenticated, DocumentPermission]

class ProjectListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = ProjectSerializer
    pagination_class = pagination.PageNumberPagination
    pagination_class.page_size = settings.PAGE_SIZE
    permission_classes = [IsAuthenticated, ProjectPermission]

    def get_queryset(self):
        queryset = Project.objects.all()
        queryset = queryset.order_by('-created_at')
        return queryset

class ProjectRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated, ProjectPermission]

class ProjectSearchAPIView(APIView):
    permission_classes = [IsAuthenticated, ProjectPermission]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('search_term', openapi.IN_QUERY, type=openapi.TYPE_STRING, required=False, description='Search term to filter projects by name'),
            openapi.Parameter('status', openapi.IN_QUERY, type=openapi.TYPE_STRING, required=False, description='Filter projects by status. Possible values: backlog, todo, doing, done, blocked, archived'),
            openapi.Parameter('since', openapi.IN_QUERY, type=openapi.TYPE_STRING, required=False, description='Filter projects created since a specific date. Format: YYYY-MM-DD')
        ],
        responses={status.HTTP_200_OK: ProjectSerializer(many=True) }
    )
    def get(self, request, *args, **kwargs):
        search_term = request.query_params.get('search_term', None)
        status_query = request.query_params.get('status', None)
        since = request.query_params.get('since', None)

        projects = Project.objects.all()

        if search_term:
            projects = projects.filter(name__icontains=search_term)

        if status_query:
            if status_query not in [s[0] for s in Status.choices]:
                return Response({ 'status': 'Invalid status' }, status=status.HTTP_400_BAD_REQUEST)
            projects = projects.filter(status=status_query)

        if since:
            try:
                since = datetime.strptime(since, '%Y-%m-%d').date()
            except ValueError:
                return Response({ 'since': 'Invalid date format. Expected: YYYY-MM-DD' }, status=status.HTTP_400_BAD_REQUEST)

            projects = projects.filter(created_at__gte=since)

        projects = projects.order_by('-created_at')
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
