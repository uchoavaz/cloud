from django.contrib import admin
from .models import Droplet
from .models import UserDroplet
from .models import AvailableIps
from .models import Image


class ImageAdmin(admin.ModelAdmin):
    list_filter = ['name']
    list_display = (
        'name', 'name_path')


class DropletAdmin(admin.ModelAdmin):
    list_filter = ['title']
    list_display = (
        'title', 'memory', 'processor')


class UserDropletAdmin(admin.ModelAdmin):
    list_display = (
        'user', 'droplet')

class AvailableIpsAdmin(admin.ModelAdmin):
    search_fields = ['ip']
    list_display = (
        'ip',
        'is_available',
        'user')

admin.site.register(Image, ImageAdmin)
admin.site.register(UserDroplet, UserDropletAdmin)
admin.site.register(Droplet, DropletAdmin)
admin.site.register(AvailableIps, AvailableIpsAdmin)
