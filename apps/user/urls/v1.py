from django.urls import path

from apps.user.views.device import DeviceRegisterCreateAPIView, DeviceListApiView

app_name = 'users'

urlpatterns = [
    path('devises/', DeviceRegisterCreateAPIView.as_view(), name='device-register'),
    path('devices/list/', DeviceListApiView.as_view(), name='device-list'),
]