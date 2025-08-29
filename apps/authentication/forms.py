from django import forms
from django.contrib.auth import authenticate, get_user_model

from apps.common.utils.forms import BaseForm


class LoginForm(BaseForm):
    username = forms.CharField(
        label="Correo electrónico",
        widget=forms.EmailInput(attrs={"placeholder": "tu.correo@ejemplo.com"}),
    )
    password = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(attrs={'placeholder': 'Tu contraseña'}),
    )

    def clean(self):
        user_model = get_user_model()
        username_field = user_model.USERNAME_FIELD
        credential = {
            username_field: self.cleaned_data.get('username'),
            'password': self.cleaned_data.get('password'),
        }
        if credential:
            member = authenticate(**credential)
            print(credential)
            if not member:
                raise forms.ValidationError("Usuario y/o contraseña incorrecto")
            if not member.is_active:
                raise forms.ValidationError("Esta usuario esta inactivo, comuniquece con el encargado del sistema")
            self.cleaned_data['member'] = member
        return self.cleaned_data
