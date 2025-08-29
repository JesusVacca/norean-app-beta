from django.contrib import admin
from apps.members.models import Member, StudentProfile, TeacherProfile
# Register your models here.
admin.site.register(Member)
admin.site.register(StudentProfile)
admin.site.register(TeacherProfile)
