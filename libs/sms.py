from django.conf import settings
from django.contrib.sites import requests

from common import config


def send(phone_num,code):
    if settings.DEBUG:   #开发中debug模式走这里
        print(phone_num,code)
        return True

    params = config.YZX_SMS_PARAMS.copy()
    params['mobile'] = phone_num
    params['param'] = phone_num

    resp = requests.post(config.YZX_SMS_URL,json=params)

    if resp.status_code == 200:
        result = resp.json()
        if result.get('code') == '000000':
            return True
    return False


