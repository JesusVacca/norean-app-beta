from django.urls import path
from . import views

app_name = 'members'

urlpatterns = [
    path('', views.ListMembersView.as_view(), name='list'),
    path('create/', views.CreateMemberView.as_view(), name='create'),
    path('create-multiple-members/', views.CreateMultipleMembersByCSVView.as_view(), name='create-multiple-members'),
    path('<str:email>/change/', views.UpdateMemberView.as_view(), name='update'),
    path('<str:email>/toggle-status-member/', views.ToggleMemberStatusView.as_view(), name='toggle-status-member'),

    path('student-profile/<int:pk>/', views.StudentProfileUpdateView.as_view(), name='student-profile'),
    path('teacher-profile/<int:pk>/', views.TeacherProfileUpdateView.as_view(), name='teacher-profile'),
]