from django.contrib import admin
from .models import Droplet
from .models import UserDroplet
from .models import StateDroplet


class DropletAdmin(admin.ModelAdmin):
    list_filter = ['title']
    list_display = (
        'title', 'memory', 'processor')


class UserDropletAdmin(admin.ModelAdmin):
    list_display = (
        'user', 'droplet')

class StateDropletAdmin(admin.ModelAdmin):
    list_display = (
        'ip_3',
        'last_ip_4',
        'last_droplet_id',
        'pool_ip',
        'available_ip')

admin.site.register(UserDroplet, UserDropletAdmin)
admin.site.register(Droplet, DropletAdmin)
admin.site.register(StateDroplet, StateDropletAdmin)
