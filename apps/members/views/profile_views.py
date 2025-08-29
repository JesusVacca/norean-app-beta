from apps.common.utils.decorators import requires_permission
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ( UpdateView )

from apps.members.models import StudentProfile, TeacherProfile
from apps.members.forms import StudentProfileForm, TeacherProfileForm
from apps.common.utils.decorators import requires_permission


@method_decorator(requires_permission('student_profile.change_studentprofile'), name='dispatch')
class StudentProfileUpdateView(UpdateView):
    model = StudentProfile
    template_name = 'recycle/create.html'
    form_class = StudentProfileForm
    success_url = reverse_lazy('management:members:list')
    def get_context_data(self, **kwargs):
        context = super(StudentProfileUpdateView, self).get_context_data(**kwargs)
        context['text_button'] = 'Actualizar perfil estudiante'
        return context


class TeacherProfileUpdateView(UpdateView):
    model = TeacherProfile
    template_name = 'recycle/create.html'
    form_class = TeacherProfileForm
    success_url = reverse_lazy('management:members:list')
    def get_context_data(self, **kwargs):
        context = super(TeacherProfileUpdateView, self).get_context_data(**kwargs)
        context['text_button'] = 'Actualizar datos del perfil'
        return context