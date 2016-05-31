
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^criar$', views.droplets, name='droplets'),
    url(r'^lista$',
        views.lista,
        name='list'),
    url(r'^remover/droplet/(?P<pk>\d+)$',
        views.remove_droplet,
        name='remove_droplet'),

    url(r'^editar/droplet/(?P<pk>\d+)/$',
        views.edit_droplet,
        name='edit_droplet'),

    url(r'^editar/droplet/(?P<pk>\d+)/nova-senha/$',
        views.new_password_droplet,
        name='new_password_droplet'),
]
