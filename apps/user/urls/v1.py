from django.urls import path

from apps.user.views.user_create import UserRegisterAPIView
from apps.user.views.user_list import CarListAPIView

app_name = 'users'

urlpatterns = [
    path('', CarListAPIView.as_view(), name='list'),
    # path('<int:car_id>/rent/', CarRentCreateAPIView.as_view(), name='rent'),
]