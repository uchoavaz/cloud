
# -*- coding: utf-8 -*-
from django import forms
from .models import CloudUser


class ProfileForm(forms.ModelForm):
    class Meta:
        model = CloudUser
        fields = (
            'full_name',
            'username',
            'email',)


class PasswordForm(forms.ModelForm):
    password1 = forms.CharField(
        label=("Nova Senha"),
        widget=forms.PasswordInput,
        help_text='Insira a senha')
    password2 = forms.CharField(
        label=(u"Confirmação da nova senha"),
        widget=forms.PasswordInput)

    class Meta:
        model = CloudUser
        fields = ('password1', 'password2')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(u'Senhas não coincidem')
        return password2

    def save(self, commit=True):
        user = super(PasswordForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
