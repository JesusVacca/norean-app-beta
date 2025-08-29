from django.urls import path, include
from . import views

app_name = 'management'

urlpatterns = [

    path('', include('apps.core.urls')),
    path('members/', include('apps.members.urls', namespace='members')),
    path('classrooms/', include('apps.classroom.urls', namespace='classrooms')),
    path('inventory/', include('apps.inventory.urls', namespace='inventory')),
    path('roles-permissions/', view=views.RolesAndPermissionsView.as_view(), name='roles-permissions'),
    path('roles-permissions/create/', view=views.RolesAndPermissionsCreateView.as_view(), name='roles-permissions-create'),
]