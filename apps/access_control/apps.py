from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class AccessControlConfig(AppConfig):
    name = 'apps.access_control'
    verbose_name = _('Access controls')
