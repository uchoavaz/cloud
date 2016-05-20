
# -*- coding: utf-8 -*-
from django.shortcuts import redirect
from django.core.urlresolvers import reverse_lazy
from django.views.generic import ListView
from django.views.generic import RedirectView
from django.views.generic import DeleteView
from .models import Droplet
from .models import AvailableIps
from .models import UserDroplet
from .models import Image
from .tasks import create_vm
from .tasks import remove_vm
from django.contrib import messages
from django.http import HttpResponseRedirect


class DropletsView(ListView):
    template_name = "droplets.html"
    model = Droplet

    def get_context_data(self, **kwargs):
        context = super(DropletsView, self).get_context_data(**kwargs)
        context['images'] = Image.objects.all()
        return context

    def dispatch(self, request, *args, **kwargs):
        if self.request.GET:
            droplet = int(self.request.GET.get('droplet'))
            image = int(self.request.GET.get('image'))
            self.create_droplet(droplet, image)
            return redirect(reverse_lazy('vm:list'))
        else:
            return super(
                DropletsView, self).dispatch(
                request, *args, **kwargs)

    def create_droplet(self, droplet, image):
        droplet = Droplet.objects.get(pk=droplet)
        image = Image.objects.get(pk=image)
        ip_disponivel = AvailableIps.objects.filter(is_available=True)

        if ip_disponivel.exists():

            ip = ip_disponivel[0].ip
            name = ip_disponivel[0].ip
            ip_disponivel.filter(ip=ip).update(is_available=False)

            UserDroplet.objects.create(
                user=self.request.user,
                droplet=droplet,
                image=image,
                ip=ip,
                name=name,
                status=3
            )

            create_vm.delay(name, ip, droplet, image)
            messages.success(
                self.request, '{0} está sendo criada !'.format(ip))

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
                ip_disponivel.filter(ip=ip).update(is_available=False)

                UserDroplet.objects.create(
                    user=self.request.user,
                    droplet=droplet,
                    ip=ip,
                    name=name,
                    status=3
                )

                create_vm.delay(name, ip, droplet)
            messages.success(
                self.request, '{0} está sendo criada !'.format(ip))
            return redirect(url)


class RemoveDropletView(DeleteView):
    model = UserDroplet
    success_url = reverse_lazy('vm:list')

    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)


    def delete(self, *args, **kwargs):
        user_droplet = UserDroplet.objects.get(pk=self.kwargs.get('pk'))
        ip = user_droplet.ip
        remove_vm.delay(user_droplet.name)
        user_droplet.delete()
        messages.success(self.request, '{0} excluída com sucesso !'.format(ip))
        return HttpResponseRedirect(reverse_lazy('vm:list'))


droplets = DropletsView.as_view()
lista = ListView.as_view()
create_droplet = CreateDropletView.as_view()
remove_droplet = RemoveDropletView.as_view()
