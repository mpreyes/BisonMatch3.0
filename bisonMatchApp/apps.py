from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _

class BisonmatchappConfig(AppConfig):
    name = 'bisonMatchApp'
    verbose_name = _('bison_match_app')

    def ready(self):
        print("got the signal!")
        import bisonMatchApp.signals
