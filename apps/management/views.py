import json

from django.contrib.contenttypes.models import ContentType
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView
from django.contrib.auth.models import Group, Permission

from apps.management.forms import RoleForm
# Create your views here.


APPS_NAME = ['members']
class RolesAndPermissionsView(TemplateView):
    template_name = 'management/roles-permissions.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        groups = Group.objects.all()
        groups = groups.order_by('name')
        context['groups'] = groups
        return context


class RolesAndPermissionsCreateView(CreateView):
    template_name = 'recycle/create.html'
    success_url = reverse_lazy('management:roles-permissions')
    model = Group
    form_class = RoleForm
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['text_button'] = 'Crear grupo'
        return context

    def form_valid(self, form):
        form.instance.name = form.cleaned_data['name'].upper()
        if Group.objects.filter(name=form.instance.name).exists():
            form.add_error('name', 'Ya existe un grupo con ese nombre')
        return super().form_valid(form)


