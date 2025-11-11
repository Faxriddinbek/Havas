from apps.shared.exceptions.custom_exceptions import CustomException
from apps.user.model.devise_model import Device


class AddCustomHeaderMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # ⚙️ Standart qiymatlarni oldindan berib qo'yamiz
        request.device_type = "UNKNOWN"
        request.lang = "uz"

        device_token = request.headers.get('Token')
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')

        # ⚙️ MOBILE dan kelgan bo‘lsa
        if device_token:
            request.device_type = "MOBILE"
            try:
                device = Device.objects.get(device_token=device_token)
                request.lang = str(device.language).lower()
            except Device.DoesNotExist:
                raise CustomException(message_key="NOT_FOUND")

        # ⚙️ WEB dan kelgan bo‘lsa
        elif auth_header:
            request.device_type = "WEB"
            request.lang = request.headers.get('Accept-Language', 'uz')

        response = self.get_response(request)
        return response
