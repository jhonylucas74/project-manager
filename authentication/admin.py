from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
class GroupInline(admin.StackedInline):
    model = CustomUser.groups.through
    extra = 0

class CustomUserAdmin(UserAdmin):
	model = CustomUser
	inlines = [GroupInline]
	list_display = ('email', 'name', 'is_active', 'is_staff', 'created_at', 'updated_at')
	fieldsets = (
		('Personal Info', {'fields': ('email', 'name',)}),
		('Permissions', {'fields': ('is_active', 'is_staff')}),
	)
	add_fieldsets = (
		(None, {
			'classes': ('wide',),
			'fields': ('email', 'name', 'password1', 'password2', 'is_active', 'is_staff')}
		),
	)
	search_fields = ('email', 'name')
	ordering = ('email',)


admin.site.register(CustomUser, CustomUserAdmin)