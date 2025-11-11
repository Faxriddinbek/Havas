from rest_framework import serializers

from apps.list.models import ListTitle, ListModel


class ListTitleSerializer(serializers.ModelSerializer):
    color_display = serializers.CharField(source='get_color_display', read_only=True)# read_only faqat o'qish uchun post putlar ishlamaydi

    class Meta:
        model = ListTitle
        fields = ['id', 'title', 'color', 'color_display']


class ListModelSerializer(serializers.ModelSerializer):
    shopping_list_title = serializers.CharField(source='shopping_list.title', read_only=True)
    shopping_list_color = serializers.CharField(source='shopping_list.color', read_only=True)
    product_name = serializers.CharField(source='product.title', read_only=True)
    unit_display = serializers.CharField(source='get_unit_display', read_only=True)

    class Meta:
        model = ListModel
        fields = [
            'id',
            'shopping_list',
            'shopping_list_title',
            'shopping_list_color',
            'product_name',
            'quantity',
            'unit',
            'unit_display',
            'is_selected'
        ]
