import logging

from django.utils.deprecation import MiddlewareMixin

from libs.http import render_json
from common import stat

err_logger = logging.getLogger('err')


class AuthMiddleware(MiddlewareMixin):
    '''登录验证中间件'''
    white_list = [
        '/',
        '/api/user/vcode/fetch',
        '/api/user/vcode/submit',
        '/qiniu/callback',
    ]

    def process_request(self, request):
        # 检查当前接口是否在白名单中
        if request.path in self.white_list:
            return

        uid = request.session.get('uid')
        if uid is None:
            return render_json(code=stat.LoginRequired.code)
        else:
            request.uid = uid


class LogicErrMiddleware(MiddlewareMixin):
    '''逻辑异常处理中间件'''

    def process_exception(self, request, err):
        if isinstance(err, stat.LogicErr):
            err_logger.error(f'LogicErr: {err.data} ({err.code})')
            return render_json(err.data, err.code)
