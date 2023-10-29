import time
import json
from urllib.parse import urlencode

from qiniu import Auth

from swiper import config as cfg


def gen_policy(uid, key):
    '''产生一个上传策略'''
    url = '%s/%s' % (cfg.QN_HOST, key)
    return {
        'scope': f"{cfg.QN_BUCKET}:{key}",
        'deadline': int(time.time()) + 3600 * 8 + cfg.QN_TIMEOUT,
        'returnBody': json.dumps({'code': 0, 'data': url}),
        'callbackUrl': 'http://demo.seamile.cn/qiniu/callback',
        'callbackHost': 'demo.seamile.cn',
        'callbackBody': urlencode({'uid': uid, "key": key}),
        'callbackBodyType': 'application/x-www-form-urlencoded',
        'forceSaveKey': True,
        'saveKey': key,
        'fsizeLimit': 10485760,  # 10 MB
        'mimeLimit': 'image/*',
    }


def get_token(uid, key):
    '''产生一个上传凭证 (Token)'''
    qn_auth = Auth(cfg.QN_ACCESS_KEY, cfg.QN_SECRET_KEY)
    policy = gen_policy(uid, key)
    token = qn_auth.upload_token(cfg.QN_BUCKET, key, cfg.QN_TIMEOUT, policy)
    return token
