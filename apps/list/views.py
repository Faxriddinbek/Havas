from rest_framework import viewsets, status, generics
from rest_framework.decorators import action

from apps.list.models import ListModel, ListTitle
from apps.list.serializer import ListModelSerializer, ListTitleSerializer
from apps.shared.utils.custom_response import CustomResponse


class ShoppingListItemViewSet(viewsets.ModelViewSet):
    """
    Mahsulotlarni to'liq boshqarish
    GET /api/items/
    POST /api/items/
    GET /api/items/1/
    PUT /api/items/1/
    PATCH /api/items/1/
    DELETE /api/items/1/
    """
    queryset = ListModel.objects.all()
    serializer_class = ListModelSerializer

    @action(detail=True, methods=['patch'])
    def toggle_selected(self, request, pk=None):
        """
        Mahsulotni tanlangan/tanlanmagan qilish
        PATCH /api/items/1/toggle_selected/
        """
        item = self.get_object()
        item.is_selected = not item.is_selected
        item.save()
        serializer = self.get_serializer(item)
        return CustomResponse.success(
            message_key='SUCCESS_MESSAGE',
            data=serializer.data,
            status_code=status.HTTP_201_CREATED
        )

    @action(detail=False, methods=['delete'])
    def clear_selected(self, request):
        """
        Barcha tanlangan mahsulotlarni o'chirish
        DELETE /api/items/clear_selected/
        """
        ListModel.objects.filter(is_selected=True).delete()
        return


class ListTitleViewSet(viewsets.ModelViewSet):
    """
    Spiska yaratish, olish, o'zgartirish, o'chirish
    GET /api/lists/
    POST /api/lists/
    GET /api/lists/1/
    PUT /api/lists/1/
    DELETE /api/lists/1/
    """
    queryset = ListTitle.objects.all()
    serializer_class = ListTitleSerializer

    @action(detail=True, methods=['get'])
    def items(self, request, pk=None):
        """
        Spiskadagi barcha mahsulotlar
        GET /api/lists/1/items/
        """
        list_title = self.get_object()
        items = list_title.items.all()
        serializer = ListModelSerializer(items, many=True)
        return CustomResponse.success(
            message_key='SUCCESS_MESSAGE',
            data=serializer.data,
            status_code=status.HTTP_200_OK
        )

class ShoppingListDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Bitta mahsulotni olish, o'zgartirish, o'chirish
    GET /api/items/1/
    PUT /api/items/1/
    DELETE /api/items/1/
    """
    queryset = ListModel.objects.all()
    serializer_class = ListModelSerializer

class ShoppingListItemListView(generics.ListCreateAPIView):
    """
    Barcha mahsulotlarni olish va yangi mahsulot qo'shish
    GET /api/items/
    POST /api/items/
    """
    queryset = ListModel.objects.all()
    serializer_class = ListModelSerializer