from django.apps import AppConfig


class AgadmatorConfig(AppConfig):
    name = 'agadmator'

    def ready(self):
        # noinspection PyUnresolvedReferences
        from . import signals
