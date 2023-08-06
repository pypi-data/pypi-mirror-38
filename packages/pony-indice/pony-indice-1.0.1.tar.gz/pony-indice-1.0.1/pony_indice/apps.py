from django.apps import AppConfig


class PonyIndiceConfig(AppConfig):
    name = 'pony_indice'
    verbose_name = "Pony Indice"

    def ready(self):
        from pony_indice import registry
