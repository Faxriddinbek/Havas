from django.urls import path

from apps.user.views.device import DeviceRegisterCreateAPIView

app_name = 'users'

urlpatterns = [
    path('devises/', DeviceRegisterCreateAPIView.as_view(), name='device-register'),
]