
# -*- coding: utf-8 -*-
from django.shortcuts import redirect
from django.core.urlresolvers import reverse_lazy
from django.views.generic import ListView
from django.views.generic import RedirectView
from django.views.generic import DeleteView
from .models import Droplet
from .models import AvailableIps
from .models import UserDroplet
from .tasks import create_vm
from .tasks import remove_vm


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


class CreateDropletView(RedirectView):
    url = reverse_lazy('vm:list')

    def get(self, request, *args, **kwargs):
        url = self.get_redirect_url(**kwargs)
        if url:

            droplet = Droplet.objects.get(pk=self.kwargs.get('pk'))
            ip_disponivel = AvailableIps.objects.filter(is_available=True)

            if ip_disponivel.exists():

                ip = ip_disponivel[0].ip
                name = ip_disponivel[0].ip

                create_vm.delay(name, ip, droplet)

                ip_disponivel.filter(ip=ip).update(is_available=False)

                UserDroplet.objects.create(
                    user=self.request.user,
                    droplet=droplet,
                    ip=ip,
                    name=name,
                    is_active=True
                )
            return redirect(url)


class RemoveDropletView(DeleteView):
    model = UserDroplet
    success_url = reverse_lazy('vm:list')

    def get(self, *args, **kwargs):
        vm_name = self.get_queryset().get().name
        remove_vm.delay(vm_name)
        return self.post(*args, **kwargs)

droplets = DropletsView.as_view()
lista = ListView.as_view()
create_droplet = CreateDropletView.as_view()
remove_droplet = RemoveDropletView.as_view()
