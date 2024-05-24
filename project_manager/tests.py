from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from authentication.models import CustomUser
from .models import Project


class DocumentProjectCRUDTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.project_data = {'name': 'Test Project', 'description': 'Test Description'}
        self.user_data = {
            'email': 'test@example.com',
            'password': 'testpassword',
            'name': 'Test User',
            'is_superuser': True,
        }
        self.user = CustomUser.objects.create_user(**self.user_data)
        refresh = RefreshToken.for_user(self.user)
        self.headers = { 'Authorization': f'Bearer {refresh.access_token}' }

    def test_document_crud(self):
        # Create Project
        project = Project.objects.create(**self.project_data)

        # Create Document
        with open('README.md', 'rb') as file:
            document_data = { 'project_id': project.id, 'file': file }
            create_response = self.client.post(reverse('document-list-create'), document_data, format='multipart', headers=self.headers)
            self.assertEqual(create_response.status_code, status.HTTP_201_CREATED)
            document_id = create_response.data['data']['id']

        # Retrieve Document
        retrieve_response = self.client.get(reverse('document-detail', args=[document_id]), headers=self.headers)
        self.assertEqual(retrieve_response.status_code, status.HTTP_200_OK)

        # Update Document
        updated_document_data = {'name': 'Updated Document', 'extension': 'pdf'}
        update_response = self.client.put(reverse('document-detail', args=[document_id]), updated_document_data, format='json', headers=self.headers)
        self.assertEqual(update_response.status_code, status.HTTP_200_OK)
        self.assertEqual(update_response.data['name'], updated_document_data['name'])

        # Delete Document
        delete_response = self.client.delete(reverse('document-detail', args=[document_id]), headers=self.headers)
        self.assertEqual(delete_response.status_code, status.HTTP_204_NO_CONTENT)

    def test_project_crud(self):
        # Create Project
        create_response = self.client.post(reverse('project-list-create'), self.project_data, format='json', headers=self.headers)
        self.assertEqual(create_response.status_code, status.HTTP_201_CREATED)
        project_id = create_response.data['id']

        # Retrieve Project
        retrieve_response = self.client.get(reverse('project-detail', args=[project_id]), headers=self.headers)
        self.assertEqual(retrieve_response.status_code, status.HTTP_200_OK)

        # Update Project
        updated_project_data = {'name': 'Updated Project', 'description': 'Updated Description'}
        update_response = self.client.put(reverse('project-detail', args=[project_id]), updated_project_data, format='json', headers=self.headers)
        self.assertEqual(update_response.status_code, status.HTTP_200_OK)
        self.assertEqual(update_response.data['name'], updated_project_data['name'])

        # Delete Project
        delete_response = self.client.delete(reverse('project-detail', args=[project_id]), headers=self.headers)
        self.assertEqual(delete_response.status_code, status.HTTP_204_NO_CONTENT)

    def test_milestone_crud(self):
        # Create Project
        project = Project.objects.create(**self.project_data)

        # Create Milestone
        create_response = self.client.post(reverse('milestone-list-create'), {'name': 'Test Milestone', 'project': project.id}, format='json', headers=self.headers)
        self.assertEqual(create_response.status_code, status.HTTP_201_CREATED)
        milestone_id = create_response.data['id']

        # Retrieve Milestone
        retrieve_response = self.client.get(reverse('milestone-detail', args=[milestone_id]), headers=self.headers)
        self.assertEqual(retrieve_response.status_code, status.HTTP_200_OK)

        # Update Milestone
        updated_milestone_data = {'name': 'Updated Milestone', 'description': 'Updated Description'}
        update_response = self.client.put(reverse('milestone-detail', args=[milestone_id]), updated_milestone_data, format='json', headers=self.headers)
        self.assertEqual(update_response.status_code, status.HTTP_200_OK)
        self.assertEqual(update_response.data['name'], updated_milestone_data['name'])

        # Delete Milestone
        delete_response = self.client.delete(reverse('milestone-detail', args=[milestone_id]), headers=self.headers)
        self.assertEqual(delete_response.status_code, status.HTTP_204_NO_CONTENT)

    def test_task_crud(self):
        # Create Project
        project = Project.objects.create(**self.project_data)

        # Create Task
        create_response = self.client.post(reverse('task-list-create'), {'name': 'Test Task', 'project': project.id}, format='json', headers=self.headers)
        self.assertEqual(create_response.status_code, status.HTTP_201_CREATED)
        task_id = create_response.data['id']

        # Retrieve Task
        retrieve_response = self.client.get(reverse('task-detail', args=[task_id]), headers=self.headers)
        self.assertEqual(retrieve_response.status_code, status.HTTP_200_OK)

        # Update Task
        updated_task_data = {'name': 'Updated Task', 'description': 'Updated Description'}
        update_response = self.client.put(reverse('task-detail', args=[task_id]), updated_task_data, format='json', headers=self.headers)
        print(update_response.data)
        self.assertEqual(update_response.status_code, status.HTTP_200_OK)
        self.assertEqual(update_response.data['name'], updated_task_data['name'])

        # Delete Task
        delete_response = self.client.delete(reverse('task-detail', args=[task_id]), headers=self.headers)
        self.assertEqual(delete_response.status_code, status.HTTP_204_NO_CONTENT)