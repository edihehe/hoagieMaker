from django.apps import AppConfig

class LunchConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'lunch'

    def ready(self):
        import lunch.signals  # Import signals ONLY when apps are ready
