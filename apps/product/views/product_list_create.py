from rest_framework import status
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import AllowAny

from apps.product.models import Product
from apps.product.serializers.product_create import ProductCreateSerializer
from apps.shared.utils.custom_pagination import CustomPageNumberPagination
from apps.shared.utils.custom_response import CustomResponse


class ProductListCreateAPIView(ListCreateAPIView):
    parser_classes = [AllowAny]
    pagination_class = CustomPageNumberPagination
    serializer_class = ProductCreateSerializer
    queryset = Product.objects.filter(is_active = True)

    def list(self, request, *args, **kwargs):
        pass

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return CustomResponse.error(
                message_key='VALIDATION_ERROR',
                errors=serializer.errors
            )
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return CustomResponse.success(
            message_key='SUCCESS_MESSAGE',
            data=serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )
