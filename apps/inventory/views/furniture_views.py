from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import (CreateView, ListView, DetailView, UpdateView)
from django.utils.decorators import method_decorator

from apps.inventory.models import Furniture
from apps.inventory.forms import FurnitureForm
from apps.common.utils.decorators import requires_permission

@method_decorator(requires_permission('inventory.add_furniture'), name='dispatch')
class CreateFurnitureView(CreateView):
    model = Furniture
    template_name = 'recycle/create.html'
    form_class = FurnitureForm
    success_url = reverse_lazy('management:inventory:furniture')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['text_button'] = 'Crear mobiliario'
        context['go_back'] = reverse_lazy('management:inventory:furniture')
        return context


@method_decorator(requires_permission('inventory.view_furniture'), name='dispatch')
class ListFurnitureView(ListView):
    model = Furniture
    template_name = 'inventory/list.html'
    context_object_name = 'furnitures'
    paginate_by = 10


@method_decorator(requires_permission('inventory.view_furniture'), name='dispatch')
class DetailFurnitureView(DetailView):
    model = Furniture
    template_name = 'inventory/detailfurniture.html'
    object_name = 'furniture'
    slug_field = 'code'
    slug_url_kwarg = 'code'

@method_decorator(requires_permission('inventory.change_furniture'), name='dispatch')
class UpdateFurnitureView(UpdateView):
    model = Furniture
    form_class = FurnitureForm
    template_name = 'recycle/create.html'
    success_url = reverse_lazy('management:inventory:furniture')
    slug_field = 'code'
    slug_url_kwarg = 'code'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['text_button'] = 'Actualizar mobiliario'
        context['go_back'] = reverse_lazy('management:inventory:furniture')
        return context