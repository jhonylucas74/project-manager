from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission

def get_permissions(codenames):
	"""
	Returns a list of permissions
	"""
	return Permission.objects.filter(codename__in=codenames)

def get_permission(codename):
	"""
	Returns a permission
	"""
	return Permission.objects.get(codename=codename)

def add_permissions():
	"""
	Adds permissions to the groups
	"""
	member_group = Group.objects.get(name='Member')
	manager_group = Group.objects.get(name='Manager')
	owner = Group.objects.get(name='Owner')
	groups = [member_group, manager_group, owner]
	manager_groups = [manager_group, owner]

	view_permissions = get_permissions(['view_project', 'view_document'])
	upload_doc_permission = get_permission('add_document')
	change_doc_permission = get_permission('change_document')
	delete_doc_permission = get_permission('delete_document')
	create_project_permission = get_permission('add_project')
	change_project_permission = get_permission('change_project')
	delete_project_permission = get_permission('delete_project')

	for group in manager_groups:
		group.permissions.add(change_doc_permission)
		group.permissions.add(delete_doc_permission)
		group.permissions.add(create_project_permission)
		group.permissions.add(change_project_permission)

	# Add the delete project permission to the owner group
	owner.permissions.add(delete_project_permission)

	for group in groups:
		# Add the upload document permission to all groups
		group.permissions.add(upload_doc_permission)

		# Add the view permissions to all groups
		for permission in view_permissions:
			group.permissions.add(permission)

class Command(BaseCommand):
	help = "A command to assign permissions to groups"

	def handle(self, *args, **kwargs):
		self.stdout.write("Assigning permissions to groups...")
		add_permissions()
		self.stdout.write(self.style.SUCCESS("Permissions assigned successfully!"))





