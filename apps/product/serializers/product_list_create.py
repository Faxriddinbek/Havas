from rest_framework import serializers

from apps.product.models import Product
from apps.shared.mixins.translation_mixins import (
    TranslatedFieldsWriteMixin,
    TranslatedFieldsReadMixin
)


class ProductTranslationMixin:
    """Bu klass Product serializerlari uchun umumiy konfiguratsiya beradi."""
    translatable_fields = ['title', 'description'] # buyerda nimalar tarjima bo'lishini kiritish kerak
    media_fields = ['image']# buyerda medifilelar xam tarima qilinishni anglatadi


class ProductCreateSerializer(ProductTranslationMixin, TranslatedFieldsWriteMixin, serializers.ModelSerializer):# product yaratilayotganda serializatsiya qilish
    class Meta:
        model = Product
        fields = ['title', 'description', 'price', 'measurement_type',
                  'is_active', 'category', 'discount']

    # def create(self, validated_data):
    #     request = self.context.get('request')# bu viewda bergan contextdan requestni oladi
    #     if request and hasattr(request, 'user'):# buyerda request kelyaptimi va requestda user nomli atribut borligini tekshiradi bo'masa xatolik qaytaradi
    #         validated_data['created_by'] = request.user # buyerda created_by ga userni bazada qo'shadi
    #     return super().create(validated_data)# buyerda saqlaydi


class ProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        exclude = ['title', 'description']


class ProductDetailSerializer(ProductTranslationMixin, TranslatedFieldsReadMixin, serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'uuid', 'title', 'description',
                  'price', 'real_price', 'measurement_type',
                  'created_at', 'is_active', 'category', 'discount']