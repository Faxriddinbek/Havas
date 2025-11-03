from django.db.models.signals import pre_save
from django.dispatch import receiver

from apps.product.models import Product


@receiver(pre_save, sender=Product) # bu funksiya model saqlashdan oldin ishlayadi
def update_real_price_field(sender, instance, **kwargs): # instance bu saqlayotgan product obyektini qaytaradi (sender > signal yuborgan model)
    if instance.discount > 0:# bu productda chegirma bor yoqligini qaytaradi
        instance.real_price = instance.price - (instance.price / 100 * instance.discount) # bu real_priceni hisoblaydi