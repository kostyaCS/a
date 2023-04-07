"""
Module for app registration.
"""
from django.apps import AppConfig


class MainMenuConfig(AppConfig):
    """
    This class register app.
    """
    default_auto_field = "django.db.models.BigAutoField"
    name = "main_menu"
