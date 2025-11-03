from rest_framework import status
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny

from apps.product.models import Product
from apps.product.serializers.product_list_create import ProductCreateSerializer, ProductDetailSerializer
from apps.shared.utils.custom_pagination import CustomPageNumberPagination
from apps.shared.utils.custom_response import CustomResponse


class ProductListCreateApiView(ListCreateAPIView):# bu get va post metodlarini qo'llab quvvatlaydi
    serializer_class = ProductCreateSerializer# bu serializatsiyadan o'tkazadi
    pagination_class = CustomPageNumberPagination # paginatsuya qiladi
    permission_classes = [IsAuthenticated]# login qilgan qilmaganni tekshiradi

    def get_queryset(self):
        return Product.objects.filter(is_active=True)# bu product bazada bor yoki yoqligini tekshiradi

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})# foydalanuvhci yuborgan ma'lumotlarni serializer qiladi
        if serializer.is_valid():# yuborilgan ma'lumotlar to'g'ri yoki yo'qligini tekshiradi
            product = serializer.save()# ma'lumotni bazaga saqlaydi
            response_serializer = ProductDetailSerializer(product, context={'request': request})# yaratilgan productni API javobiga mos holatga o'zgartiradi
            return CustomResponse.success( # CustomResponse da ehtimoliy javoblar tayyorlangan
                message_key="SUCCESS_MESSAGE",# qaysi javob qaytarilish kerakligini kiritadi
                data=response_serializer.data,
                status_code=status.HTTP_201_CREATED
            )
        else:
            return CustomResponse.error(# agar validatsiyadan o'tmas error qaytaradi
                message_key="VALIDATION_ERROR",
                errors=serializer.errors
            )
