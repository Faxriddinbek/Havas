from django.db import models
from apps.user.model.user_model import BaseModel, User
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import AuthenticationFailed

class DeviseModel(BaseModel):
    devise_id = models.CharField(max_length=255, unique=True)
    devise_model = models.CharField(max_length=255)
    language = models.CharField(max_length=255)
    devise_version = models.CharField(max_length=255)
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)

    def get_tokens(self):
        if not self.is_active:
            raise AuthenticationFailed("User is not active")

        refresh = RefreshToken.for_user(self)

        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }







#devise_id
#devise_model, language, devise_vesion, jwt_token, user   jpt(i just wonna create jwt )
 