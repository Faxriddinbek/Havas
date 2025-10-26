from rest_framework import serializers

from apps.shared.exceptions.custom_exceptions import CustomException
from apps.user.model.devise_model import DeviseModel
from apps.user.model.user_model import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class DeviseModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeviseModel
        fields = ['devise_id', 'devise_model', 'language', 'devise_version']

    def validate(self, attrs):
        devise_id = attrs.get('devise_id')
        if devise_id:
            raise CustomException(
                message_key="device_already_exists"
            )