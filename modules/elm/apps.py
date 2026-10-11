# ELM module initialization
from django.apps import AppConfig

class ElmAppConfig(AppConfig):
    name = 'modules.elm'
    label = 'elm'

    def ready(self):
        import modules.elm.signals # noqa