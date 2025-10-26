from django.contrib.auth.models import AbstractUser
from django.db import models
from rest_framework.views import APIView


class BaseModel(models.Model):
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True

class User(AbstractUser, BaseModel):
    phone_number = models.CharField(max_length=255, unique=True)

