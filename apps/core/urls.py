from django.urls import path
from . import views
app_name = 'core'

urlpatterns = [
    path('dashboard/', view=views.DashboardView.as_view(), name='dashboard'),
]