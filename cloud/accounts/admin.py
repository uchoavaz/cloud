from django.contrib import admin
from .models import CloudUser


class CloudUserAdmin(admin.ModelAdmin):
    list_filter = ['email']
    list_display = (
        'email', 'is_staff',
        'is_active', 'is_superuser')


admin.site.register(CloudUser, CloudUserAdmin)
