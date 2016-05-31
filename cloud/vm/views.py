
# -*- coding: utf-8 -*-
from django.shortcuts import redirect
from django.core.urlresolvers import reverse_lazy
from django.views.generic import ListView
from django.views.generic import DeleteView
from .models import Droplet
from .models import AvailableIps
from .models import UserDroplet
from .models import Image
from accounts.models import CloudUser
from .tasks import create_vm
from .tasks import remove_vm
from .tasks import edit_vm
from .tasks import new_password_vm
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from .utils import id_generator
from django.views.generic import RedirectView


class BaseView(LoginRequiredMixin):
    login_url = reverse_lazy("core:login")

    def get_context_data(self, **kwargs):
        context = super(BaseView, self).get_context_data(**kwargs)
        context['my_cash'] = CloudUser.objects.get(
            pk=self.request.user.pk).cash
        return context


class DropletsView(BaseView, ListView):
    template_name = "droplets.html"
    model = Droplet

    def get_queryset(self):
        queryset = super(DropletsView, self).get_queryset().order_by('disk')
        return queryset

    def get_context_data(self, **kwargs):
        context = super(DropletsView, self).get_context_data(**kwargs)
        context['images'] = Image.objects.all()
        return context

    def dispatch(self, request, *args, **kwargs):
        if self.request.GET:
            droplet = int(self.request.GET.get('droplet'))
            image = int(self.request.GET.get('image'))
            user_cash = self.request.user.cash
            droplet_cost = self.get_queryset().get(pk=droplet).cost

            if user_cash >= droplet_cost:
                self.create_droplet(droplet, image)

                final_cash = user_cash - droplet_cost
                CloudUser.objects.filter(pk=self.request.user.pk).update(
                    cash=final_cash)
                return redirect(reverse_lazy('vm:list'))
            else:
                messages.error(
                    self.request, "Você não tem créditos suficientes !")

            return redirect(reverse_lazy('vm:droplets'))
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

            user_droplet = UserDroplet.objects.create(
                user=self.request.user,
                droplet=droplet,
                image=image,
                ip=ip,
                name=name,
                status=3
            )
            create_vm.delay(
                name, ip,
                droplet, image,
                id_generator(),
                user_droplet.user.username, user_droplet.user.email)

            messages.success(
                self.request, '{0} está sendo criada !'.format(ip))
            messages.success(
                self.request, 'Sua senha será enviada para {0} !'.format(
                    user_droplet.user.email))
        else:
            messages.error(
                self.request, 'Sem IP disponível')


class ListView(BaseView, ListView):
    template_name = "list.html"
    model = UserDroplet


class RemoveDropletView(BaseView, DeleteView):
    model = UserDroplet
    success_url = reverse_lazy('vm:list')

    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)

    def delete(self, *args, **kwargs):
        user_droplet = UserDroplet.objects.get(pk=self.kwargs.get('pk'))
        ip = user_droplet.ip
        cost_droplet = user_droplet.droplet.cost
        user_cash = self.request.user.cash
        final_cash = user_cash + cost_droplet
        CloudUser.objects.filter(pk=self.request.user.pk).update(
            cash=final_cash)
        remove_vm.delay(user_droplet.name)
        user_droplet.delete()
        messages.success(self.request, '{0} excluída com sucesso !'.format(ip))
        return HttpResponseRedirect(reverse_lazy('vm:list'))


class EditDropletView(ListView, BaseView):
    template_name = "edit.html"
    model = Droplet

    def user_droplet(self):
        user_droplet = UserDroplet.objects.get(pk=self.kwargs.get('pk'))
        return user_droplet

    def get_queryset(self):
        user_droplet = self.user_droplet()
        queryset = super(EditDropletView, self).get_queryset().filter(
            disk__gt=user_droplet.droplet.disk).order_by('disk')
        return queryset

    def get_context_data(self, **kwargs):
        context = super(EditDropletView, self).get_context_data(**kwargs)
        context['user_droplet'] = self.user_droplet()
        return context

    def dispatch(self, request, *args, **kwargs):
        if self.request.GET:
            id_droplet = int(self.request.GET.get('droplet'))
            intended_droplet = Droplet.objects.get(pk=id_droplet)
            atual_droplet = UserDroplet.objects.get(pk=self.kwargs.get('pk'))

            atual_droplet_cost = atual_droplet.droplet.cost
            intended_droplet_cost = intended_droplet.cost
            user_cash = self.request.user.cash

            if not intended_droplet.disk <= atual_droplet.droplet.disk:

                if (user_cash + atual_droplet_cost) >= intended_droplet_cost:
                    self.edit_droplet(
                        intended_droplet, atual_droplet, id_droplet)

                    final_cash = (
                        user_cash + atual_droplet_cost) - intended_droplet_cost
                    CloudUser.objects.filter(pk=self.request.user.pk).update(
                        cash=final_cash)
                    messages.success(
                        self.request, '{0} está sendo alterada !'.format(
                            atual_droplet.ip))
                else:
                    messages.error(
                        self.request, "Você não tem cŕeditos suficientes !")
            else:
                messages.error(
                    self.request, u'{0} não pode diminuir seu disco !'.format(
                        atual_droplet.ip))

            return redirect(reverse_lazy('vm:list'))

        else:
            return super(
                EditDropletView, self).dispatch(
                request, *args, **kwargs)

    def edit_droplet(self, intended_droplet, atual_droplet, id_droplet):
        ip = atual_droplet.ip
        cpu = intended_droplet.processor
        memory = intended_droplet.memory
        disk = intended_droplet.disk
        name = ip
        UserDroplet.objects.filter(ip=ip).update(
            droplet=id_droplet, can_remove=False, status=4)
        edit_vm.delay(ip, cpu, memory, name, disk)


class NewPasswordView(ListView):
    url = reverse_lazy('vm:list')

    def get(self, request, *args, **kwargs):
        user_droplet = UserDroplet.objects.get(pk=self.kwargs.get('pk'))
        ip = user_droplet.ip
        name = ip
        cpu = user_droplet.droplet.processor
        memory = user_droplet.droplet.memory
        new_password = id_generator()
        username = user_droplet.user.username
        email = user_droplet.user.email
        UserDroplet.objects.filter(ip=ip).update(can_remove=False, status=4)

        messages.success(
            self.request, "Sua nova senha vai ser enviada para {0}".format(
                email))

        new_password_vm.delay(
            name, ip, cpu, memory, new_password, username, email)
        return redirect(self.url)


droplets = DropletsView.as_view()
lista = ListView.as_view()
remove_droplet = RemoveDropletView.as_view()
edit_droplet = EditDropletView.as_view()
new_password_droplet = NewPasswordView.as_view()
