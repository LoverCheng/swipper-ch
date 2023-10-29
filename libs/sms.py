import json
import time
from hashlib import md5

import requests

from swiper import config as cfg


def send_sms(phonenum, vcode):
    '''发送验证码'''
    # 构造参数
    args = {
        'appid': cfg.SD_APPID,
        'to': phonenum,
        'project': cfg.SD_PROJECT,
        'vars': json.dumps({"vcode": vcode}),
        'timestamp': int(time.time()),
        'sign_type': cfg.SD_SIGN_TYPE,
    }

    # 计算签名
    signature_str = '&'.join([f'{k}={v}' for k, v in sorted(args.items())])
    string = f'{cfg.SD_APPID}{cfg.SD_APPKEY}{signature_str}{cfg.SD_APPID}{cfg.SD_APPKEY}'
    signature = md5(string.encode('utf8')).hexdigest()

    # 将签名添加到参数列表中
    args['signature'] = signature

    response = requests.post(cfg.SD_API, data=args)
    result = response.json()
    print(result)
    return result
