from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class PartnerConfig(AppConfig):
    name = 'partner'
    verbose_name = _(' Partners')
