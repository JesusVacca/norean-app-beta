from django.db.models import Q
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import (CreateView, ListView, UpdateView)


from apps.common.utils.decorators import requires_permission
from apps.classroom.forms.classroom_form import ClassroomForm
from apps.classroom.models import Classroom
# Create your views here.

@method_decorator(requires_permission('classroom.add_classroom'), name='dispatch')
class ClassroomCreateView(CreateView):
    model = Classroom
    form_class = ClassroomForm
    success_url = reverse_lazy('management:classroom:list')
    template_name = 'members/../../templates/recycle/create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['text_button'] = 'Agregar Aula Física'
        context['go_back'] = reverse_lazy('management:classroom:list')
        return context

@method_decorator(requires_permission('classroom.view_classroom'), name='dispatch')
class ClassroomListView(ListView):
    model = Classroom
    template_name = 'classroom/list.html'
    context_object_name = 'classrooms'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search'] = self.request.GET.get('search','')
        return context

    def get_queryset(self):
        queryset = Classroom.objects.all()
        search = self.request.GET.get('search','')
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(label__icontains=search) |
                Q(classroom_manager__member__first_name__icontains=search)
            )
        return queryset


@method_decorator(requires_permission('classroom.change_classroom'), name='dispatch')
class ClassroomUpdateView(UpdateView):
    model = Classroom
    form_class = ClassroomForm
    success_url = reverse_lazy('management:classroom:list')
    slug_field = 'pk'
    slug_url_kwarg = 'pk'
    template_name = 'members/../../templates/recycle/create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['text_button'] = 'Actualizar Aula Física'
        context['go_back'] = reverse_lazy('management:classroom:list')
        return context