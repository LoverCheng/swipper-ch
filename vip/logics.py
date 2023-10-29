from common.stat import PermErr
from user.models import User


def require_perm(perm_name):
    def deco(view_func):
        def wrapper(request, *args, **kwargs):
            user = User.objects.get(id=request.uid)  # 取出当前用户

            # 检查用户权限
            if user.vip.has_perm(perm_name):
                response = view_func(request, *args, **kwargs)
                return response
            else:
                raise PermErr
        return wrapper
    return deco
