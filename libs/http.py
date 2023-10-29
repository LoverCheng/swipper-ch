import json

from django.http import HttpResponse
from django.conf import settings


def render_json(data=None, code=0):
    '''前后端接口定义'''
    result = {
        'data': data,
        'code': code
    }

    if settings.DEBUG == True:
        # 调试时，将 json 数据转成带缩进的格式
        json_str = json.dumps(result, ensure_ascii=False, indent=4, sort_keys=True)
    else:
        # 线上环境，将返回值转成紧凑格式
        json_str = json.dumps(result, ensure_ascii=False, separators=(',', ':'))

    return HttpResponse(json_str, content_type='application/json')
