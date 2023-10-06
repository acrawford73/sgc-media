from django.contrib import admin

from .models import SystemConfig

class SystemConfigAdmin(admin.ModelAdmin):
	list_display = ['version']
	readonly_fields = ['created', 'updated']
	class Meta:
		model = SystemConfig

# Register with Admin
admin.site.register(SystemConfig, SystemConfigAdmin)
