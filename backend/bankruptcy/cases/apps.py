from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class CasesConfig(AppConfig):
    name = 'bankruptcy.cases'
    verbose_name = _('Cases')

    def ready(self):
        try:
            import bankruptcy.cases.signals  # noqa F401
        except ImportError:
            pass
