from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.list.views import ShoppingListItemViewSet, ShoppingListDetailView, ListTitleViewSet

router = DefaultRouter()
router.register(r'lists', ListTitleViewSet)
router.register(r'items', ShoppingListItemViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('items/', ShoppingListItemViewSet.as_view()),
    path('items/<int:pk>/', ShoppingListDetailView.as_view()),
]