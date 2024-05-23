from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import Project

class DocumentProjectCRUDTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.project_data = {'name': 'Test Project', 'description': 'Test Description'}

    def test_document_crud(self):
        # Create Project
        project = Project.objects.create(**self.project_data)

        # Create Document
        with open('readme.md', 'rb') as file:
            document_data = { 'project_id': project.id, 'file': file }
            create_response = self.client.post(reverse('document-list-create'), document_data, format='multipart')
            self.assertEqual(create_response.status_code, status.HTTP_201_CREATED)
            document_id = create_response.data['data']['id']

        # Retrieve Document
        retrieve_response = self.client.get(reverse('document-detail', args=[document_id]))
        self.assertEqual(retrieve_response.status_code, status.HTTP_200_OK)

        # Update Document
        updated_document_data = {'name': 'Updated Document', 'extension': 'pdf'}
        update_response = self.client.put(reverse('document-detail', args=[document_id]), updated_document_data, format='json')
        self.assertEqual(update_response.status_code, status.HTTP_200_OK)
        self.assertEqual(update_response.data['name'], updated_document_data['name'])

        # Delete Document
        delete_response = self.client.delete(reverse('document-detail', args=[document_id]))
        self.assertEqual(delete_response.status_code, status.HTTP_204_NO_CONTENT)

    def test_project_crud(self):
        # Create Project
        create_response = self.client.post(reverse('project-list-create'), self.project_data, format='json')
        self.assertEqual(create_response.status_code, status.HTTP_201_CREATED)
        project_id = create_response.data['id']

        # Retrieve Project
        retrieve_response = self.client.get(reverse('project-detail', args=[project_id]))
        self.assertEqual(retrieve_response.status_code, status.HTTP_200_OK)

        # Update Project
        updated_project_data = {'name': 'Updated Project', 'description': 'Updated Description'}
        update_response = self.client.put(reverse('project-detail', args=[project_id]), updated_project_data, format='json')
        self.assertEqual(update_response.status_code, status.HTTP_200_OK)
        self.assertEqual(update_response.data['name'], updated_project_data['name'])

        # Delete Project
        delete_response = self.client.delete(reverse('project-detail', args=[project_id]))
        self.assertEqual(delete_response.status_code, status.HTTP_204_NO_CONTENT)
