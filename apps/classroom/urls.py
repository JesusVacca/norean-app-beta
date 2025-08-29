from django.urls import path
from . import views

app_name = 'classroom'
urlpatterns = [
    path('', views.ClassroomListView.as_view(), name='list'),
    path('<int:pk>/change/', views.ClassroomUpdateView.as_view(), name='update'),
    path('create/', views.ClassroomCreateView.as_view(), name='create'),
]