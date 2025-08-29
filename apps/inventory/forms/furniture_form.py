from apps.common.utils.forms import BaseModelForm
from apps.inventory.models import Furniture


class FurnitureForm(BaseModelForm):
    class Meta:
        model = Furniture
        fields = [
            'name',
            'status',
            'notes',
            'materials'
        ]
        labels = {
            'name':'Nombre provicional',
            'status':'Estado del elemento',
            'notes':'Notas',
            'materials':'Materiales del elemento'
        }