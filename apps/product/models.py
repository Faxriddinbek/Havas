from django.contrib.contenttypes.fields import GenericRelation
from django.db import models

from apps.shared.models import BaseModel


class MeasurementType(models.TextChoices):# bu product ni vazni
    GR = "GR", "Gram"
    PC = "PC", "Peace"
    L = "L", "Litre"


class ProductCategory(models.TextChoices): # Catigoriyasi
    BREAKFAST = "BREAKFAST", "Breakfast"
    LUNCH = "LUNCH", "Lunch"
    DINNER = "DINNER", "Dinner"
    ALL = "ALL", "All"


class Product(BaseModel):
    media_files = GenericRelation(
        'shared.Media',
        related_query_name='products'
    )
    title = models.CharField(max_length=255, db_index=True) # db_index=True titleni search qilishni tezlashtiradi
    description = models.TextField()

    discount = models.PositiveSmallIntegerField(default=0)# bu chegirma fildi
    price = models.DecimalField(max_digits=30, decimal_places=2)
    real_price = models.DecimalField(max_digits=30, decimal_places=2)# bu chegirmadan keyingi narxi

    category = models.CharField( # Product catigoriyaga bog'lanadi
        choices=ProductCategory, default=ProductCategory.ALL,
        db_index=True
    )
    measurement_type = models.CharField( #Productni Vaznini ifodalydi
        choices=MeasurementType, default=MeasurementType.GR
    )
    is_active = models.BooleanField(default=True)# bu product bazada bor yoqligini tekshiradi (True yoki False qaytaradi)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'product'
        verbose_name_plural = 'products'