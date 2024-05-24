from rest_framework import permissions

class ProjectPermission(permissions.BasePermission):
    def has_permission(self, request, obj):
        if request.user.is_superuser:
            return True

        if request.method:
            if request.method == 'POST':
                return request.user.has_perm('project_manager.add_project')
            if request.method == 'PUT':
                return request.user.has_perm('project_manager.change_project')
            if request.method == 'DELETE':
                return request.user.has_perm('project_manager.delete_project')
            if request.method == 'GET':
                return request.user.has_perm('project_manager.view_project')
        return False
    
class DocumentPermission(permissions.BasePermission):
    def has_permission(self, request, obj):
        if request.user.is_superuser:
            return True

        if request.method:
            if request.method == 'POST':
                return request.user.has_perm('project_manager.add_document')
            if request.method == 'PUT':
                return request.user.has_perm('project_manager.change_document')
            if request.method == 'DELETE':
                return request.user.has_perm('project_manager.delete_document')
            if request.method == 'GET':
                return request.user.has_perm('project_manager.view_document')
        return False
