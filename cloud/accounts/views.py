
from django.views.generic.edit import FormView
from django.core.urlresolvers import reverse_lazy
from django.contrib import messages
from .forms import ProfileForm
from .forms import PasswordForm
from .models import CloudUser
from django.shortcuts import redirect
from vm.views import BaseView


class ProfileView(BaseView, FormView):
    template_name = 'profile.html'
    form_class = ProfileForm
    success_url = reverse_lazy('accounts:profile')

    def get_form(self, form_class):
        user = CloudUser.objects.get(email=self.request.user.email)
        return form_class(instance=user, **self.get_form_kwargs())

    def form_valid(self, form, **kwargs):
        form.instance.user = self.request.user
        form.save()

        messages.success(self.request, 'Seu perfil foi atualizado')
        return redirect(self.success_url)


class PasswordView(BaseView, FormView):
    template_name = 'password.html'
    form_class = PasswordForm
    success_url = reverse_lazy('core:home')

    def get_form(self, form_class):
        user = CloudUser.objects.get(email=self.request.user.email)
        return form_class(instance=user, **self.get_form_kwargs())

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.save()
        messages.success(
            self.request,
            'Sua senha foi alterada! Entre no sistema com sua nova senha')
        return super(PasswordView, self).form_valid(form)


profile = ProfileView.as_view()
password = PasswordView.as_view()
