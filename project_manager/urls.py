from django.urls import path
from .views import DocumentUploadListView, ProjectListCreateAPIView, ProjectRetrieveUpdateDestroyAPIView, DocumentRetrieveUpdateDestroyAPIView, ProjectSearchAPIView, MilestoneListCreateAPIView, MilestoneRetrieveUpdateDestroyAPIView, TaskListCreateAPIView, TaskRetrieveUpdateDestroyAPIView

urlpatterns = [
    path('documents/upload/', DocumentUploadListView.as_view(), name='document-upload'),
    path('documents/', DocumentUploadListView.as_view(), name='document-list-create'),
    path('documents/<int:pk>/', DocumentRetrieveUpdateDestroyAPIView.as_view(), name='document-detail'),
    path('projects/', ProjectListCreateAPIView.as_view(), name='project-list-create'),
    path('projects/<int:pk>/', ProjectRetrieveUpdateDestroyAPIView.as_view(), name='project-detail'),
    path('projects/search/', ProjectSearchAPIView.as_view(), name='project-search'),
    path('milestones/', MilestoneListCreateAPIView.as_view(), name='milestone-list-create'),
    path('milestones/<int:pk>/', MilestoneRetrieveUpdateDestroyAPIView.as_view(), name='milestone-detail'),
    path('tasks/', TaskListCreateAPIView.as_view(), name='task-list-create'),
    path('tasks/<int:pk>/', TaskRetrieveUpdateDestroyAPIView.as_view(), name='task-detail'),
]
