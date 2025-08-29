from django.contrib.auth.models import Group
from django import forms
from apps.common.utils.forms import BaseModelForm

class RoleForm(BaseModelForm):

    class Meta:
        model = Group
        fields = [
            'name',
            'permissions'
        ]