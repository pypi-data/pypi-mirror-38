from django.utils.translation import ugettext_lazy as _


class SMSModuleException(Exception):

    default_message = _('A module error occurred.')
    default_code = '_error'

    def __init__(self, code=None, message=None):
        self.code = code or self.default_code
        self.message = message or self.default_message

    def __str__(self):
        return f'<{self.__class__.__name__} code: {self.code} message: {self.message}>'


class RequestNotReachable(SMSModuleException):

    default_message = _('Not reachable. Connection timeout')
    default_code = '_timeout'


class ReceivedErrorResponse(SMSModuleException):

    default_message = _('Received unknown error. Check please.')
    default_code = '_unknown'
