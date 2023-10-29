'''前后端的状态码'''

OK = 0  # 正常


class LogicErr(Exception):
    code = OK
    data = None

    def __init__(self, err_data=None):
        super().__init__()
        self.data = err_data or self.__class__.__name__


def gen_logic_err(name, code):
    '''生成一个新的 LogicErr 子类'''
    return type(name, (LogicErr,), {'code': code})


SendFaild = gen_logic_err('SendFaild', 1000)          # 验证码发送失败
VocdeErr = gen_logic_err('VocdeErr', 1001)            # 验证码错误
LoginRequired = gen_logic_err('LoginRequired', 1002)  # 需要用户登陆
ProfileErr = gen_logic_err('ProfileErr', 1003)        # 用户、资料表单数据错误
SidErr = gen_logic_err('SidErr', 1004)                # SID错误
StypeErr = gen_logic_err('StypeErr', 1005)            # 滑动类型错误
SwipeRepeat = gen_logic_err('SwipeRepeat', 1006)      # 重复滑动
RewindLimited = gen_logic_err('RewindLimited', 1007)  # 反悔次数达到限制
RewindTimeout = gen_logic_err('RewindTimeout', 1008)  # 反悔超时
NoSwipe = gen_logic_err('NoSwipe', 1009)              # 当前还没有滑动记录
PermErr = gen_logic_err('PermErr', 1010)              # 用户不具有某权限
