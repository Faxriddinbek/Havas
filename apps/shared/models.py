from django.db import models
import uuid
from django.contrib.contenttypes.models import ContentType
from django.db import models

class Language(models.TextChoices):
    RU = "RU", "Russian"
    EN = "EN", "English"
    CRL = "CRL", "Cyrillic"
    UZ = "UZ", "Uzbek"

#  ORM (Object Relational Mapper)
class BaseModel(models.Model):
    """
    UUID asosiy kalit (primary key) va vaqt tamg‘asi (timestamp) maydonlariga ega abstrakt asosiy model
    """
    uuid = models.UUIDField( # uuid takrorlanmas string generatsiya qilib beradi
        default=uuid.uuid4, # har safar yangi obyect yaratilganda UUid generatsiya qilsdi
        editable=False, # Buni adminpanel yoki format orqali taxrirlab bo'lmaydi
        db_index=True # bu malumotlar bazasida index yaratadi (qidiruv tezligini ohirish uchun)
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ['-created_at']