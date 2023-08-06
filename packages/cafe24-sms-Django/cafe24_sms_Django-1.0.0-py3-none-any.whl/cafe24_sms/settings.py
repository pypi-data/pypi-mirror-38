from __future__ import with_statement

from django.conf import settings
from django.test.signals import setting_changed
from django.utils.translation import ugettext_lazy as _


MODULE_SETTINGS_NAME = 'CAFE24_SMS_SETTINGS'

DEFAULTS = {
    # Required
    'USER_ID': None,
    'SECURE_KEY': None,
    'SENDER': None,

    # Optional
    'REQUEST_TIMEOUT': 30.0,
    'TEST_MODE': False,
    'CHARSET': 'euc-kr',
    'TIMEZONE': 'Asia/Seoul',
}


class Cafe24SMSSettings:

    def __init__(self, defaults=None, custom_settings=None):
        self.defaults = defaults or DEFAULTS
        if custom_settings:
            self._custom_settings = custom_settings

    @property
    def custom_settings(self):
        if not hasattr(self, '_custom_settings'):
            self._custom_settings = getattr(settings, MODULE_SETTINGS_NAME, {})
        return self._custom_settings

    def __getattr__(self, attr):
        if attr not in self.defaults:
            raise AttributeError(_('Invalid setting "%s"' % attr))

        try:
            return self.custom_settings[attr]
        except KeyError:
            return self.defaults[attr]

    def reload(self):
        if hasattr(self, '_custom_settings'):
            delattr(self, '_custom_settings')


module_settings = Cafe24SMSSettings(DEFAULTS, None)


def reload_api_settings(*args, **kwargs):
    setting = kwargs['setting']
    if setting == MODULE_SETTINGS_NAME:
        module_settings.reload()


setting_changed.connect(reload_api_settings)
