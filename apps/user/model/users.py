from datetime import timedelta

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from rest_framework_simplejwt.tokens import RefreshToken

from apps.shared.models import BaseModel
from apps.user.manager.user import CustomUserManager


class User(AbstractBaseUser, PermissionsMixin, BaseModel): # AbstractBaseUser menga pasvord va last_login beradi va buni ishlarganda PermissionsMixin ishlatish kerak
    """
    Custom user model with flexible authentication fields
    """

    # Bular hohlagan 3 tasidan 1 tasi orqali login qilsam bo'ladi
    email = models.EmailField(
        max_length=255, unique=True, null=True,
        blank=True, db_index=True
    )

    username = models.CharField(
        max_length=150, unique=True, null=True,
        blank=True, db_index=True
    )

    phone_number = models.CharField(
        max_length=17, unique=True, null=True,
        blank=True, db_index=True
    )

    # Profile fields (Userni ma'lumotlari)
    first_name = models.CharField(max_length=64, blank=True, null=True)
    last_name = models.CharField(max_length=64, blank=True, null=True)
    middle_name = models.CharField(max_length=64, blank=True, null=True)
    date_of_birth = models.DateField(null=True, blank=True)

    # Status fields
    is_active = models.BooleanField(default=False) #activligini tekshiradi
    is_email_verified = models.BooleanField(default=False) #email verifikatsiyadanligini tekshiradi
    is_phone_verified = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = CustomUserManager()

    # This field is used for authentication
    USERNAME_FIELD = 'phone_number'  # Default to phone_number, but can authenticate with any
    REQUIRED_FIELDS = []  # No required fields since we have flexible auth

    class Meta:
        db_table = 'users'
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        indexes = [# indexes bu foydalanuvchilar email, username, phone_number orqali qidiradigon qismi
            models.Index(fields=['email'], name='users_email_idx'),
            models.Index(fields=['username'], name='users_username_idx'),
            models.Index(fields=['phone_number'], name='users_phone_idx')
        ]
        constraints = [
            models.CheckConstraint( # bu foydalanuvchida shu uchtasidan kamida 1 tasi bo'lishi kerak
                check=models.Q(email__isnull=False) |# agar bo'lmasa foydalanuvchini bazada saqlab bo'lmaydi
                      models.Q(username__isnull=False) |
                      models.Q(phone_number__isnull=False),
                name='user_must_have_identifier'
            )
        ]

    @property # metodlarni atribut qilib beradi
    def full_name(self):
        """
        Return the full name for the user
        """
        return f"{self.first_name} {self.last_name}".strip()

    def __str__(self):
        if self.username:
            return self.username
        elif self.phone_number:
            return self.phone_number

        return self.email

    def get_tokens(self, access_lifetime=None, refresh_lifetime=None): # user yaratgandan keyin .get_tokens deb olsa bo'ladi
        """Generate JWT tokens for the user with optional custom expiration"""
        refresh = RefreshToken.for_user(self)

        # Set custom lifetimes if provided
        if access_lifetime:
            refresh.access_token.set_exp(lifetime=access_lifetime)
        if refresh_lifetime:
            refresh.set_exp(lifetime=refresh_lifetime)

        # Add custom claims
        refresh['email'] = self.email
        refresh['username'] = self.username
        refresh['user_id'] = self.id

        expires_at = timezone.now() + timedelta(seconds=refresh.access_token.lifetime.total_seconds())
        refresh_expires_at = timezone.now() + timedelta(seconds=refresh.lifetime.total_seconds())# life_timeni hisoblash

        return {
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'token_type': 'Bearer',
            'expires_at': expires_at.isoformat(),
            'refresh_expires_at': refresh_expires_at.isoformat(),
        }