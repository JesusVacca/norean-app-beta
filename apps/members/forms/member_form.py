from django import forms
from django.contrib.auth.models import Group

from apps.common.utils.forms import BaseModelForm
from apps.common.utils.choices import MemberRoleChoices
from apps.members.models import Member


class MemberForm(BaseModelForm):
    aux_passwod = forms.CharField(widget=forms.PasswordInput(
        attrs={'placeholder': 'Ingresa una contraseña'}),
        label='Contraseña',
        required=True
    )
    groups = forms.ModelMultipleChoiceField(
        queryset=Group.objects.none(),
        required=True,
        widget=forms.SelectMultiple,
        label='Grupos de usuarios',
    )

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['groups'].queryset = (
                Group.objects.all()
                if user.is_superuser or ( user.has_perm('members.add_superadmin') and user.has_perm('members.add_admin') )
                else
                Group.objects.filter(name__in=[MemberRoleChoices.TEACHER, MemberRoleChoices.STUDENT])
            )
        if self.instance and self.instance.pk:
            self.fields['aux_passwod'].required = False

    def save(self, commit=True, created_by = None):
        member = super().save(commit=False)
        aux_passwod = self.cleaned_data['aux_passwod']
        groups = self.cleaned_data['groups']
        if aux_passwod:
            member.set_password(aux_passwod)
        if created_by:
            member.created_by = created_by
        if commit:
            member.save()
        if groups:
            member.groups.set(groups)
        return member

    def clean_phone_number(self):
        phone_number = self.cleaned_data['phone_number']
        if not Member.objects.validate_phone_format(phone_number):
            raise forms.ValidationError(
                "Número de teléfono inválido. Debe comenzar con 3 y tener 10 dígitos numéricos."
                "Formato esperado: 3XXXXXXXXX (Ejemplo: 3117984622)."
            )
        return phone_number

    def clean_email(self):
        email = self.cleaned_data['email']
        qs = Member.objects.filter(email=email)
        if self.instance and self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError("Este correo electrónico ya está registrado. Por favor, usa uno diferente.")
        return email

    def clean_document_number(self):
        document_number = self.cleaned_data['document_number']
        qs = Member.objects.filter(document_number=document_number)
        if self.instance and self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError('El número de documento que ingresaste ya está en uso. Por favor, verifica la información.')
        return document_number



    class Meta:
        model = Member
        fields = [
            'first_name',
            'last_name',
            'phone_number',
            'document_type',
            'document_number',
            'groups',
            'email',
            'aux_passwod'
        ]
        labels = {
            'first_name': 'Nombres',
            'last_name': 'Apellidos',
            'phone_number': 'Número de telefono',
            'document_type': 'Tipo de documento',
            'document_number': 'Número de documento',
            'email': 'Correo electrónica',
            'password': 'Contraseña',
        }