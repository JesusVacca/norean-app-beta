import pandas as pd
from urllib.parse import urlencode

from apps.common.utils.choices import MemberRoleChoices
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ( CreateView, ListView, UpdateView, View )
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_POST
from django.contrib.auth.models import Group


from apps.members.models import Member
from apps.members.forms import MemberForm, MultipleMembersByCSVForm
from apps.common.utils.decorators import requires_permission
from apps.common.utils.notify import Notify

notify = Notify()


@method_decorator(requires_permission('members.add_member'), name='dispatch')
class CreateMemberView(CreateView):
    model = Member
    form_class = MemberForm
    template_name = 'recycle/create.html'
    success_url = reverse_lazy('management:members:list')

    def form_valid(self, form):
        form.save(created_by=self.request.user)
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['text_button'] = 'Crear usuario'
        context['subtitle'] = 'Para crear un usuario, por favor llenar todos los campo requeridos'
        return context


@method_decorator(requires_permission('members.view_member'), name='dispatch')
class ListMembersView(ListView):
    model = Member
    template_name = 'members/list.html'
    context_object_name = 'members'
    paginate_by = 10
    def get_queryset(self):
        search = self.request.GET.get('search', "")
        selected_role = self.request.GET.get('selected_role', "")
        queryset = Member.objects.all().exclude(document_number=self.request.user.document_number)
        if not self.request.user.is_superuser:
            queryset = queryset.filter(groups__name__in=[MemberRoleChoices.STUDENT, MemberRoleChoices.STUDENT])
        if search:
            queryset = queryset.filter(
                Q(first_name__icontains=search) |
                Q(last_name__icontains=search) |
                Q(email__icontains=search) |
                Q(document_number__contains=search)
            )
        if selected_role:
            queryset = queryset.filter(groups__name=selected_role)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search']  = self.request.GET.get('search', "")
        context['selected_role']  = self.request.GET.get('selected_role', "")
        context['groups_user'] = Group.objects.all()
        return context

@method_decorator(requires_permission('members.change_member'), name='dispatch')
class UpdateMemberView(UpdateView):
    model = Member
    form_class = MemberForm
    template_name = 'recycle/create.html'
    success_url = reverse_lazy('management:members:list')
    slug_field = 'email'
    slug_url_kwarg = 'email'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['text_button'] = 'Actualizar usuario'
        return context

@method_decorator(requires_permission('members.change_member'), name='dispatch')
@method_decorator(require_POST, name='dispatch')
class ToggleMemberStatusView(View):
    def post(self, request, *args, **kwargs):
        search = self.request.GET.get('search', "")
        selected_role = self.request.GET.get('selected_role', "")
        base_url = reverse('management:members:list')
        params = {}
        if search:
            params['search'] = search
        if selected_role:
            params['selected_role'] = selected_role
        try:
            member = Member.objects.get(email=kwargs['email'])
            member.is_active = not member.is_active
            member.save()
        except Member.DoesNotExist:
            pass
        return HttpResponseRedirect(f'{base_url}?{urlencode(params)}')










