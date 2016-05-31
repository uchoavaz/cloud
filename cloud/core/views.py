
# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.contrib.auth import authenticate
from django.core.urlresolvers import reverse_lazy
from django.contrib import auth
from django.shortcuts import redirect
from accounts.models import CloudUser
from vm.models import UserDroplet
from vm.views import BaseView
from django.contrib import messages
from django.views.generic.base import TemplateView


def login(request):

    context = {}

    email = request.POST.get('email')
    password = request.POST.get('password')

    context['email_label'] = CloudUser._meta.get_field(
        "email").verbose_name.title()
    context['password_label'] = CloudUser._meta.get_field(
        "password").verbose_name.title()

    if email and password:
        user = authenticate(email=email, password=password)

        if user is not None:
            if user.is_active:
                auth.login(request, user)
                return redirect(reverse_lazy('core:home'))
            else:
                messages.error(request, u'Usuário não está ativo')
        else:
            messages.error(request, u'Usuário ou senha não existente')
    return render(request, 'login.html', context)


def logout(request):
    auth.logout(request)
    return redirect(reverse_lazy('core:login'))


class HomeView(BaseView, TemplateView):
    template_name = 'home.html'
    login_url = reverse_lazy('core:login')

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['my_machines'] = UserDroplet.objects.filter(
            user=self.request.user).count()
        context['home'] = True
        return context

home = HomeView.as_view()
