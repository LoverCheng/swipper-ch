import re
import random
import logging

from django.conf import settings

from libs.sms import send_sms
from libs.cache import rds
from common import keys
from tasks import celery_app

inf_logger = logging.getLogger('inf')
P_PHONENUM = re.compile(r'^1[3456789]\d{9}$')


def is_phonenum(phonenum):
    '''检查是否是一个有效的手机号'''
    return True if P_PHONENUM.match(phonenum) else False


def gen_randcode(length):
    '''产生一个指定长度的随机码'''
    chars = random.choices('0123456789', k=length)
    return ''.join(chars)


@celery_app.task
def send_vcode(phonenum):
    '''向用户手机发送验证码'''
    key = keys.VCODE_K % phonenum

    # 检查15分钟内是否为该用户发送过验证码
    if rds.get(key):
        return True

    vcode = gen_randcode(6)  # 定义验证码
    result = send_sms(phonenum, vcode)  # 发送验证码

    if result.get('status') == 'success':
        rds.set(key, vcode, 900)  # 多为用户保留 5 分钟
        return True
    else:
        if settings.DEBUG:
            # 调试时即使发送失败，也在缓存中保存一下
            rds.set(key, vcode, 900)
            inf_logger.debug('vcode: %s' % vcode)

        return False
