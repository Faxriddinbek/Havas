from rest_framework import status
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated

from apps.product.models import Product
from apps.product.serializers.product_list_create import ProductCreateSerializer, ProductDetailSerializer
from apps.shared.utils.custom_pagination import CustomPageNumberPagination
from apps.shared.utils.custom_response import CustomResponse


class ProductListCreateApiView(ListCreateAPIView):
    serializer_class = ProductCreateSerializer
    pagination_class = CustomPageNumberPagination
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Product.objects.filter(is_active=True)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            product = serializer.save()
            response_serializer = ProductDetailSerializer(product, context={'request': request})
            return CustomResponse.success(
                message_key="SUCCESS_MESSAGE",
                data=response_serializer.data,
                status_code=status.HTTP_201_CREATED
            )
        else:
            return CustomResponse.error(
                message_key="VALIDATION_ERROR",
                errors=serializer.errors
            )