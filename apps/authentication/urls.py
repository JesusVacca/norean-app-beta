from django.urls import path
from . import views

app_name = 'authentication'

urlpatterns = [
    path('', views.LoginView.as_view(), name='login'),
    path('logout', views.LogoutView.as_view(), name='logout'),
    path('permission-denied', views.PermissionDeniedView.as_view(), name='permission-denied'),
]