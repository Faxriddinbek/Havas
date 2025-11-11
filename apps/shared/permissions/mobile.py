from rest_framework.permissions import BasePermission

from apps.shared.exceptions.custom_exceptions import CustomException
from apps.user.model.devise_model import Device


class IsMobileOrWebUser(BasePermission):# bu request web yoki mobile dan kelayotganini tekshiradi
    def has_permission(self, request, view):
        if bool(request.user and request.user.is_authenticated):# bu devise web ligini anglatadi chunki authenticated bolgan devise web hisoblanadi
            return True
        token = request.headers.get('Token')# bodydan token olish
        if not token:# token yoq bo'lsa xatolik qaytaradi
            raise CustomException(message_key="TOKEN_IS_NOT_PROVIDED")

        device = Device.objects.filter(device_token=token)
        request.device = device# bu devise mobile ekanligini bildiradi

        return device