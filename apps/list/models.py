from django.db import models

from apps.product.models import Product, MeasurementType
from apps.shared.models import BaseModel

"""
1 -class (class list )
2- class (class list(model))
3 -class 
"""


class ColorChoices(models.TextChoices):
    RED = '#ff0000', 'Qizil'
    YELLOW = '#ffff00', 'Sariq'
    BLUE = '#0000ff', 'Ko\'k'
    GREEN = '#00ff00', 'Yashil'
    ORANGE = '#ff8800', 'Apelsin'
    PINK = '#ff1493', 'Pushti'
    TEAL = '#008080', 'Firuzaviy'
    PURPLE = '#800080', 'Binafsha'
    WHITE = '#ffffff', 'Oq'


class ListTitle(BaseModel):
    title = models.CharField(max_length=255, db_index=True)
    color = models.CharField(
        max_length=7,  # hex code #xxxxxx
        choices=ColorChoices.choices,
        default=ColorChoices.WHITE,
        verbose_name='List rangi'
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "List rangi"
        verbose_name_plural = "List ranglari"


class ListModel(BaseModel):
    shopping_list = models.ForeignKey(ListTitle, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, db_index=True)
    quantity = models.IntegerField(default=1)

    unit = models.CharField(
        max_length=60,
        choices=MeasurementType.choices,
        default=MeasurementType.GR
    )
    is_selected = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.quantity} {self.unit} - {self.product.title}"

    class Meta:
        ordering = ['product__category', '-created_at']
