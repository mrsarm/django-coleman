from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class PartnerConfig(AppConfig):
    name = 'partner'
    verbose_name = _(' Partners')
