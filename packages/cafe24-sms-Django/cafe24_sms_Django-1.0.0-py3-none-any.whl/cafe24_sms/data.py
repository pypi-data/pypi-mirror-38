from django.utils.translation import ugettext_lazy as _

from .settings import module_settings
from .utils import get_local_datetime
from .utils import trans_string_to_datetime


class SMSRequestData:
    """SMSRequest data class.\n
    Instance use for Request class. :class:`cafe24_sms.request.Request`\n
    if message byte len <= 90 then SMS, len <= 2000 then LMS. (default charset 'euc-kr')
    With korean words, about 45 character SMS, more then LMS (max 1000 character).\n
    For detail, see also the Cafe24 site: `<https://www.cafe24.com/?controller=myservice_hosting_sms_example>`_.\n
    :param str message: A message data.
    :param str or list receiver: A telephone number separated by '-'.
    :param str sender: If none, use in settings sender. just same as receiver. (Optional)
    :param str title: A message title. if not none, use in LMS Type. (Optional)
    :param datetime.datetime reservation_time: Datetime to reservation. (Optional)
    :param int rpt_num: A repeat number 1 to 10. (Optional)
    :param int rpt_time: A repeat time gap. It must be set at least 15 minutes. (Optional)
    """

    def __init__(self, message, receiver, sender=None, title=None,
                 reservation_time=None, rpt_num=None, rpt_time=None, **kwargs):
        self.message = message.encode(module_settings.CHARSET)
        self.receiver = receiver
        self.title = title
        self.rpt_num = rpt_num
        self.rpt_time = rpt_time
        self.reservation_time = reservation_time

        if kwargs:
            raise TypeError(
                u"__init__ got unexpected keyword argument {}".format(
                    ', '.join(kwargs.keys())))

        default_sender = module_settings.SENDER.split('-')
        split_numbers = sender.split('-') if sender else default_sender
        base_data = {
            'user_id': module_settings.USER_ID,
            'secure': module_settings.SECURE_KEY,
            'sphone1': split_numbers[0],
            'sphone2': split_numbers[1],
        }

        if split_numbers.__len__() > 2:
            base_data.update({'sphone3': split_numbers[2]})

        if module_settings.TEST_MODE:
            base_data.update({'testflag': 'Y'})

        self.base_data = base_data

    @property
    def content(self):
        if type(self.receiver) == list:
            self.receiver = ','.join(self.receiver)

        self.base_data.update({
            'rphone': self.receiver,
            'msg': self.message,
        })

        if self.message.__len__() > 90:
            self.base_data.update({'smsType': 'L'})

            if self.title:
                # In docs, key is title. but real key is subject :(
                self.base_data.update({'subject': self.title})

        if self.rpt_num and self.rpt_time:
            self.base_data.update({
                'repeatFlag': 'Y',
                'repeatNum': self.rpt_num,
                'repeatTime': self.rpt_time,
            })

        if self.reservation_time:
            reservation_time = get_local_datetime(self.reservation_time)
            self.base_data.update({
                'rdate': reservation_time.strftime('%Y%m%d'),
                'rtime': reservation_time.strftime('%H%M%S'),
            })

        return self.base_data


class ResultCheckRequestData:
    """ResultCheckRequestData data class.\n
    Instance use for Request class. :class:`cafe24_sms.request.Request`\n
    For detail, see also the Cafe24 site: `<https://www.cafe24.com/?controller=myservice_hosting_sms_example>`_.\n

    :param datetime.datetime start_date: Check standard date
    :param int start_index: Search item start index (Optional)
    :param str send_type: Search param. sent SMS type. Choice in all, general, reserve  (Optional)
    :param str send_status: Search param. Result status. S(Success), F(Fail) (Optional)
    :param str receive_num: Search received telephone number separated by '-'. (Optional)
    :param str send_num: Search sent telephone number separated by '-'. (Optional)
    :param int check_range: Search range day (Optional)
    :param int page_limit: Result page item count (Optional)
    """

    SEND_TYPE_CHOICES = ('all', 'general', 'reserve')
    SEND_STATUS_CHOICES = ('S', 'F')

    def __init__(self, start_date, start_index=0, send_type='all', send_status='S',
                 receive_num=None, send_num=None, page_limit=20, check_range=7, **kwargs):
        self.start_date = get_local_datetime(start_date)
        self.start_index = start_index
        self.send_type = send_type
        self.send_status = send_status
        self.receive_num = receive_num
        self.send_num = send_num
        self.page_limit = page_limit
        self.check_range = check_range

        if kwargs:
            raise TypeError(
                u"__init__ got unexpected keyword argument {}".format(
                    ', '.join(kwargs.keys())))

        base_data = {
            'user_id': module_settings.USER_ID,
            'secure': module_settings.SECURE_KEY,
        }

        self.base_data = base_data

    @property
    def content(self):
        self.base_data.update({
            'date': self.start_date.strftime('%Y%m%d'),
            'day': self.check_range,
            'startNo': self.start_index,
            'displayNo': self.page_limit,
            'sendType': self.send_type,
            'sendStatus': self.send_status,
        })

        if self.receive_num:
            self.base_data.update({
                'receivePhone': self.receive_num
            })

        if self.send_num:
            self.base_data.update({
                'sendPhone': self.send_num
            })

        return self.base_data


class ResultCheckXMLData:
    """ResultCheckXMLData data class.\n
    Instance use for Request class. :class:`cafe24_sms.request.Request`\n
    For detail, see also the Cafe24 site: `<https://www.cafe24.com/?controller=myservice_hosting_sms_example>`_.\n

    :param str code: Response result code
    :param xml.etree.ElementTree.Element root: result xml root element
    """
    SEND_TYPE_CODES = {
        'R': _('예약발송'),
        'I': _('일반발송'),
    }
    SEND_STATUS_CODES = {
        '1': _('일반발송 요청'),
        '2': _('예약발송 요청'),
        '3': _('발송성공'),
        '9': _('발송실패'),
    }
    UNKNOWN = _('미분류')

    def __init__(self, code, root):
        self.code = code
        self.root = root

    def _get_send_datetime(self, date):
        return

    def get_total_count(self):
        return self.root.findtext('totalCnt', 0)

    def get_records(self):
        records = []

        for elem in self.root.iter('record'):
            send_date = trans_string_to_datetime(elem.findtext('sendDateTime'), '%Y%m%d%H%M')
            send_type = elem.findtext('sendType')
            status = elem.findtext('sendStatus')

            record = {
                'send_type': self.SEND_TYPE_CODES.get(send_type, self.UNKNOWN),
                'send_number': elem.findtext('sendPhone'),
                'receive_number': elem.findtext('receivePhone'),
                'message': elem.findtext('msg'),
                'send_datetime': send_date,
                'status': self.SEND_STATUS_CODES.get(status, self.UNKNOWN),
            }
            records.append(record)

        return records
