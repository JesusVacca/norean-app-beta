from django.urls import path
from . import views
app_name = 'inventory'
urlpatterns = [
    path('furniture/', views.ListFurnitureView.as_view(), name='furniture'),
    path('furniture/create/', views.CreateFurnitureView.as_view(), name='create-furniture'),
    path('furniture/<str:code>/', views.UpdateFurnitureView.as_view(), name='update-furniture'),
    path('furniture/<str:code>/', views.DetailFurnitureView.as_view(), name='detail-furniture'),
]