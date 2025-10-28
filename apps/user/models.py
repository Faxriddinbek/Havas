# Import all models from model package to make them discoverable by Django
from apps.user.model.users import User
from apps.user.model.devise_model import Device, AppVersion, DeviceTheme, DeviceType

__all__ = ['User', 'Device', 'AppVersion', 'DeviceTheme', 'DeviceType']