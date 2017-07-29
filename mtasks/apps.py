from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class MtasksConfig(AppConfig):
    name = 'mtasks'
    verbose_name = _(' Task Management')
