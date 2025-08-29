from re import match

from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin, Group

from apps.common.utils.choices import DocumentTypeChoices, MemberRoleChoices

class MemberManager(BaseUserManager):

    def validate_phone_format(self, phone_number):
        return bool(match(r"^3\d{9}$", phone_number) is not None)

    def create_user(self, email, password, **extra_fields):
        phone_number = extra_fields.get('phone_number')
        if not email:
            raise ValidationError('Debes proporcionar un correo electrónico valido')
        if not self.validate_phone_format(phone_number):
            raise ValidationError('El número de telefono no cumple con el formato colombiano. Ejemplo 3113123112')
        email = self.normalize_email(email)
        member = self.model(email=email, **extra_fields)
        member.set_password(password)
        member.save(using=self._db)
        return member

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        super_user =  self.create_user(email, password, **extra_fields)
        group, _ = Group.objects.get_or_create(name=MemberRoleChoices.SUPERADMIN)
        super_user.groups.add(group)
        return super_user




class Member(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    phone_number = models.CharField(max_length=10)
    email = models.EmailField(db_index=True, unique=True)
    slug = models.SlugField(max_length=100, unique=True, db_index=True, editable=False, null=True, blank=True)
    document_type = models.CharField(choices=DocumentTypeChoices.choices, max_length=10, default=DocumentTypeChoices.CC)
    document_number = models.CharField(max_length=50, db_index=True, unique=True)


    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = MemberManager()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'phone_number', 'document_number']

    def __str__(self):
        return self.first_name


    class Meta:
        verbose_name = 'Member'
        verbose_name_plural = 'Members'
        ordering = ['-created_at']
        permissions = [
            ('add_superadmin','Puede crear super administradores'),
            ('add_admin','Puede crear administradores'),
        ]

