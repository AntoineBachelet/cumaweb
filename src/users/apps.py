"""File defining the the settings of user application"""
from django.apps import AppConfig


class UsersConfig(AppConfig):
    """Config of user application"""
    default_auto_field = "django.db.models.BigAutoField"
    name = "users"
