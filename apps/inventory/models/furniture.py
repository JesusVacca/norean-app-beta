import base64
import qrcode
from io import BytesIO

from django.conf import settings
from django.db import models
from django.core.exceptions import ValidationError

from apps.common.utils.choices import FurnitureConditionChoices
from apps.common.utils.qr_code import QRCode
from apps.members.models import Member
from django.urls import reverse


class Furniture(QRCode, models.Model):
    name = models.CharField(max_length=120)
    code = models.CharField(max_length=120, unique=True, db_index=True, editable=False)
    notes = models.TextField(null=True, blank=True)
    status = models.CharField(choices=FurnitureConditionChoices.choices, max_length=12, default=FurnitureConditionChoices.GOOD)
    available = models.BooleanField(default=True)
    materials = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __generate_unique_code(self):
        from random import randint
        while True:
            code =f'{self.name[:4]}-{randint(100,999999)}'.upper()
            if not Furniture.objects.filter(code=code).exists():
                return code

    def __str__(self):
        return self.code

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = self.__generate_unique_code()
        super().save(*args, **kwargs)

    @property
    def qr_code(self):
        return super()._generate_qr_code(reverse=reverse('management:inventory:detail-furniture', kwargs={'code':self.code}))

    class Meta:
        verbose_name = 'Furniture'
        verbose_name_plural = 'Furnitures'
        ordering = ('-created_at',)



class FurnitureAssignment(models.Model):
    furniture = models.ForeignKey(Furniture, on_delete=models.CASCADE, related_name='assignments_furniture')
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='assignments_member')
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if FurnitureAssignment.objects.filter(furniture=self.furniture).count() >= 2:
            raise ValidationError('Este mueble tiene asignado 2 miembros')

    def __str__(self):
        return f'{self.furniture} - {self.member}'

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    class Meta:
        unique_together = ('furniture', 'member')
        ordering = ['-created_at']