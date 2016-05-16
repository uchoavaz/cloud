
# -*- coding: utf-8 -*-
from django.shortcuts import redirect
from django.core.urlresolvers import reverse_lazy
from django.views.generic import ListView
from .vm_lib import VM
from .models import Droplet
from .models import StateDroplet
from .models import UserDroplet
from .tasks import teste


class DropletsView(ListView):
    template_name = "droplets.html"
    model = Droplet


class ListView(ListView):
    template_name = "list.html"
    model = UserDroplet

    def get_queryset(self):
        queryset = super(ListView, self).get_queryset().filter(
            user=self.request.user)
        return queryset


def create_droplet(request, pk):
    droplet = Droplet.objects.get(pk=pk)
    state_droplet = StateDroplet.objects.all()[0]
    vm_pool = state_droplet.pool_ip
    available_ip = state_droplet.available_ip

    if available_ip > 0:
        vm_num = state_droplet.last_droplet_id
        vm_ip_3 = state_droplet.ip_3
        vm_ip_4 = state_droplet.last_ip_4

        ip = "192.168.{0}.{1}".format(vm_ip_3, vm_ip_4)
        name = "vm_{0}".format(vm_num)

        teste.delay(name, ip, droplet)

        StateDroplet.objects.all().update(
            last_droplet_id=(vm_num + 1),
            last_ip_4=(vm_ip_4 + 1),
            available_ip=(vm_pool - 1)
        )

        UserDroplet.objects.create(
            user=request.user,
            droplet=droplet,
            ip=ip,
            name=name,
            is_active=True
        )
    return redirect(reverse_lazy('vm:list'))

droplets = DropletsView.as_view()
lista = ListView.as_view()
