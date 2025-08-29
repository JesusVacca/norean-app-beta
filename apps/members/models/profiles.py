from django.db import models

class TeacherProfile(models.Model):
    member = models.OneToOneField('members.Member', on_delete=models.CASCADE, related_name='teacher_profile')
    degree = models.CharField(max_length=120, null=True, blank=True)
    institution = models.CharField(max_length=120, null=True, blank=True)
    speciality = models.CharField(max_length=120, null=True, blank=True)
    experience_years = models.PositiveIntegerField(default=0)
    cv = models.URLField(null=True, blank=True)
    is_complete = models.BooleanField(default=False, editable=False)
    def __str__(self):
        return self.member.first_name

    def save(self, *args, **kwargs):
        if self.pk:
            self.is_complete = all([
                bool(self.degree),
                bool(self.institution),
                bool(self.speciality),
                self.experience_years > 0,
                bool(self.cv)
            ])
        super().save(*args, **kwargs)

class StudentProfile(models.Model):
    member = models.OneToOneField('members.Member', on_delete=models.CASCADE, related_name='student_profile')
    guardian_name = models.CharField(max_length=120, null=True, blank=True)
    guardian_email = models.EmailField(null=True, blank=True, unique=True, db_index=True)
    guardian_phone_number = models.CharField(max_length=10, null=True, blank=True)
    is_complete = models.BooleanField(default=False, editable=False)
    def __str__(self):
        return self.member.first_name
    def save(self, *args, **kwargs):
        if self.pk:
            self.is_complete = all([
                bool(self.guardian_name),
                bool(self.guardian_email),
                bool(self.guardian_phone_number),
            ])
        super().save(*args, **kwargs)
