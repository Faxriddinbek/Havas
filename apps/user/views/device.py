from typing import Any

from rest_framework import generics, permissions, status

from apps.shared.permissions.mobile import IsMobileUser
from apps.shared.utils.custom_response import CustomResponse
from apps.user.model.devise_model import Device
from apps.user.serializers.device import DeviceRegisterSerializer


class DeviceRegisterCreateAPIView(generics.CreateAPIView):
    """
    Register device anonymously (no login required).
    Returns a device_token for future reference.
    """
    serializer_class = DeviceRegisterSerializer
    permission_classes = [permissions.AllowAny]

    def __init__(self, **kwargs: Any): # yaratilgan qurilma obyektini saqlash uchun
        super().__init__(**kwargs)
        self.device = None

    def perform_create(self, serializer): # yangi obyekt saqlash uchun ishlatiladi
        device = serializer.save() # serializer.save() bu bazaga saqlaydi
        self.device = device # o‘sha qurilma obyektini self.device da saqlab qo‘yadi.

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs) # bu CreateAPIView ni create metodini chaqiradi
        response.data['device_token'] = str(self.device.device_token)# respondi datasiga device_token generatsiya qilib saqlaydi
        return CustomResponse.success(
            message_key="SUCCESS_MESSAGE",
            data=response.data,
            status_code=status.HTTP_201_CREATED
        )


class DeviceListApiView(generics.ListAPIView):
    queryset = Device.objects.all()
    serializer_class = DeviceRegisterSerializer
    permission_classes = [IsMobileUser]

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return CustomResponse.success(
            message_key="SUCCESS_MESSAGE",
            data=serializer.data
        )