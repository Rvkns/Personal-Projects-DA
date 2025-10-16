from django.apps import AppConfig


class BundlesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "bundles"

    def ready(self):
        # Import signal handlers
        from . import signals  # noqa: F401
