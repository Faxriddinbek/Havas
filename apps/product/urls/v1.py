from django.urls import path

from apps.product.views.product_list_create import ProductListCreateAPIView

app_name = 'product'

urlpatterns = [
    path('create/', ProductListCreateAPIView.as_view(), name='product-create'),
]