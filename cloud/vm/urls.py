
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^criar$', views.droplets, name='droplets'),
    url(r'^criar/droplet/(?P<pk>\d+)$',
        'vm.views.create_droplet',
        name='create_droplet'),
    url(r'^lista$',
        views.lista,
        name='list'),
]
