from django import forms
from django.core.exceptions import ValidationError
from apps.classroom.models import Classroom
from apps.common.utils.forms import BaseModelForm


class ClassroomForm(BaseModelForm):

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get("name")
        label = cleaned_data.get("label")
        qs = Classroom.objects.filter(name=name, label=label)

        if self.instance and self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            self.add_error('name', "Ya existe un aula con ese nombre.")
            self.add_error('label', "Ya existe un aula con esa etiqueta")
        return cleaned_data

    def clean_classroom_manager(self):
        classroom_manager = self.cleaned_data.get("classroom_manager")
        if classroom_manager:
            qs = Classroom.objects.filter(classroom_manager=classroom_manager)
            if self.instance and self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise forms.ValidationError("Este docente ya esta asignado a otra aula.")
        return classroom_manager

    class Meta:
        model = Classroom
        fields = '__all__'

