from apps.common.utils.forms import BaseModelForm
from apps.members.models import TeacherProfile, StudentProfile
from django import forms


class TeacherProfileForm(BaseModelForm):
    class Meta:
        model = TeacherProfile
        exclude = ('member',)

class StudentProfileForm(BaseModelForm):
    class Meta:
        model = StudentProfile
        fields = [
            'guardian_name',
            'guardian_email',
            'guardian_phone_number',
        ]
        labels = {
            'guardian_name': 'Nombre del acudiente',
            'guardian_phone_number': 'Número de telefono del acudiente',
            'guardian_email': 'Correo electrónico del acudiente',
        }
        widgets = {
            'guardian_name': forms.TextInput(attrs={'placeholder': 'Ingresa el nombre del acudiente' }),
            'guardian_email': forms.EmailInput(attrs={'placeholder':'acudiente@ejemplo.com'}),
            'guardian_phone_number': forms.NumberInput(attrs={'placeholder':'Número de telefono ejemplo: 3127984621'}),
        }