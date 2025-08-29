from django.db import models

# Create your models here.

class Classroom(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    label = models.CharField(max_length=20, db_index=True, blank=True, null=True)
    classroom_manager = models.OneToOneField(
        'members.TeacherProfile',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    capacity = models.PositiveIntegerField(default=0)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    available = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.name}-{self.label if self.label else ""}'.capitalize()

    def save(self, *args, **kwargs):
        self.name = self.name.capitalize()
        if self.label:
            self.label = self.label.upper()
        super().save(*args, **kwargs)

    class Meta:
        ordering = ('-created_at',)
        unique_together = ('name', 'label')