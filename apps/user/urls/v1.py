from django.urls import path

from apps.user.views.device import DeviceRegisterCreateAPIView, DeviceListApiView
from apps.user.views.login import LoginView

app_name = 'users'

urlpatterns = [
    path('devices/', DeviceRegisterCreateAPIView.as_view(), name='device-register'),
    path('devices/list/', DeviceListApiView.as_view(), name='device-list'),
    path('login/', LoginView.as_view(), name='login'),
]