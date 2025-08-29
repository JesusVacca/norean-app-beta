import os
from dotenv import load_dotenv
from django.contrib.auth.models import Group
from django.db.models.signals import post_migrate, m2m_changed, post_save
from django.dispatch import receiver
from apps.members.models import Member, StudentProfile, TeacherProfile
from apps.common.utils.choices import MemberRoleChoices

load_dotenv()

data_superuser = {
    'first_name':os.getenv('FIRST_NAME'),
    'last_name':os.getenv('LAST_NAME'),
    'phone_number':os.getenv('PHONE_NUMBER'),
    'email':os.getenv('EMAIL'),
    'document_type':os.getenv('DOCUMENT_TYPE'),
    'document_number':os.getenv('DOCUMENT_NUMBER'),
    'password':os.getenv('PASSWORD'),
}


@receiver(post_migrate)
def create_default_groups(sender, **kwargs):
    if sender.name == 'apps.members':
        for value, label in MemberRoleChoices.choices:
            group, _ = Group.objects.get_or_create(name=value)


@receiver(m2m_changed, sender=Member.groups.through)
def create_profile(sender, instance, action, pk_set, **kwargs):
    if action != 'post_add':
        return
    groups = Group.objects.filter(pk__in=pk_set)
    if groups.filter(name=MemberRoleChoices.TEACHER).exists():
        if not hasattr(instance, 'teacher_profile'):
            TeacherProfile.objects.create(member=instance)
    elif groups.filter(name=MemberRoleChoices.STUDENT).exists():
        if not hasattr(instance, 'student_profile'):
            StudentProfile.objects.create(member=instance)

@receiver(m2m_changed, sender=Member.groups.through)
def member_promoted_to_superuser(sender, instance, action, pk_set, **kwargs):
    if action != 'post_add' and action != 'pos_delete' and action != 'post_clear':
        return
    groups = instance.groups.all()
    instance.is_superuser = groups.filter(name=MemberRoleChoices.SUPERADMIN).exists()
    instance.is_staff = groups.filter(name__in=[MemberRoleChoices.SUPERADMIN, MemberRoleChoices.ADMIN]).exists()
    instance.save()



@receiver(post_migrate)
def create_default_superuser(sender, **kwargs):
    if sender.name == 'apps.members':
        data_copy = data_superuser.copy()
        email = data_copy.pop('email')
        password = data_copy.pop('password')

        if not Member.objects.filter(
                email=email,
                document_number=data_copy.get('document_number')
        ).exists():
            Member.objects.create_superuser(
                email=email,
                password=password,
                **data_copy
            )
