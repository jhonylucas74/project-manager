from django.urls import path
from .views import DocumentUploadListView, ProjectListCreateAPIView, ProjectRetrieveUpdateDestroyAPIView, DocumentRetrieveUpdateDestroyAPIView

urlpatterns = [
    path('documents/upload/', DocumentUploadListView.as_view(), name='document-upload'),
    path('documents/', DocumentUploadListView.as_view(), name='document-list-create'),
    path('documents/<int:pk>/', DocumentRetrieveUpdateDestroyAPIView.as_view(), name='document-detail'),
    path('projects/', ProjectListCreateAPIView.as_view(), name='project-list-create'),
    path('projects/<int:pk>/', ProjectRetrieveUpdateDestroyAPIView.as_view(), name='project-detail'),
]
