from django.apps import AppConfig


class LoggingManagerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'logging_manager'

    def ready(self):
        import logging_manager.signals  # Ensure signals are loaded when the app is ready