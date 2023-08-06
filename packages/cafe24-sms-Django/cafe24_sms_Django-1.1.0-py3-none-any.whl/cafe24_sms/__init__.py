# -*- coding: utf-8 -*-
from __future__ import absolute_import

from pkg_resources import get_distribution

from . import exceptions
from .request import Request
from .shortcuts import send_message
from .shortcuts import reserve_message
from .shortcuts import result_check
from .result_codes import get_result_message


__version__ = get_distribution('cafe24-sms-Django').version

__all__ = (
    'result_check',
    'get_result_message',
    'reserve_message',
    'send_message',
    'exceptions',
    'Request',
)
