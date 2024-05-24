from django.db import migrations
from django.contrib.auth.models import Group

def create_groups(apps, schema_editor):
	"""
	Creates a default groups
	"""
	Group.objects.create(name='Member')
	Group.objects.create(name='Manager')
	Group.objects.create(name='Owner')

class Migration(migrations.Migration):
	dependencies = [
		('authentication', '0001_initial'),
	]

	operations = [
		migrations.RunPython(create_groups),
	]
