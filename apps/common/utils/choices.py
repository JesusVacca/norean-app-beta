from django.db import models

class DocumentTypeChoices(models.TextChoices):
    CC = "CC", "Cédula de Ciudadanía"
    TI = "TI", "Tarjeta de Identidad"
    CE = "CE", "Cédula de Extranjería"
    PA = "PA", "Pasaporte"
    NIT = "NIT", "NIT (Persona Jurídica)"
    RC = "RC", "Registro Civil"
    PEP = "PEP", "Permiso Especial de Permanencia"

class MemberRoleChoices(models.TextChoices):
    SUPERADMIN = "SUPER ADMINISTRADOR", "Super Administrador"
    ADMIN = "ADMINISTRADOR", "Administrador"
    TEACHER = "DOCENTE", "Docente"
    STUDENT = "ESTUDIANTE", "Estudiante"


class FurnitureConditionChoices(models.TextChoices):
    NEW = 'NUEVO', 'Nuevo'
    GOOD = 'BUENO', 'Bueno'
    FAIR = 'REGULAR', 'Regular'
    BAD = 'MALO', 'Malo'
    BROKEN = 'DAÑADO', 'Dañado'
    RETIRED = 'DADO DE BAJA', 'Dado de baja'
