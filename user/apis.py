import logging

from swiper import config as cfg
from libs import qn_cloud
from libs.cache import rds
from libs.http import render_json
from common import keys
from common import stat
from user import logics
from user.models import User
from user.models import Profile
from user.forms import UserForm
from user.forms import ProfileForm

inf_logger = logging.getLogger('inf')


def fetch_vcode(request):
    '''提交手机号'''
    phonenum = request.GET.get('phonenum')

    # 检查用户手机号
    if logics.is_phonenum(phonenum):
        logics.send_vcode.delay(phonenum)
        return render_json()

    raise stat.SendFaild


def submit_vcode(request):
    '''提交验证码, 完成登录、注册'''
    phonenum = request.POST.get('phonenum', '').strip()
    vcode = request.POST.get('vcode', '').strip()
    # 从缓存获取验证码
    key = keys.VCODE_K % phonenum
    cached_vcode = rds.get(key)

    # 检查验证码
    if vcode and vcode == cached_vcode:
        # 根据手机号获取用户
        try:
            user = User.objects.get(phonenum=phonenum)
            inf_logger.info(f'{user.id} login')
        except User.DoesNotExist:
            # 创建用户对象
            user = User.objects.create(phonenum=phonenum, nickname=phonenum)
            inf_logger.info(f'{user.id} register')

        # 通过 Session 记录用户登录状态
        request.session['uid'] = user.id
        return render_json(user.to_dict())
    else:
        raise stat.VocdeErr


def show_profile(request):
    '''获取交友信息'''
    uid = request.session['uid']

    key = keys.PROFILE_K % uid
    profile = rds.get(key)
    inf_logger.debug('从缓存获取数据: %s' % profile)

    if not profile:
        profile, _ = Profile.objects.get_or_create(id=uid)
        inf_logger.debug('从数据库获取数据: %s' % profile)

        inf_logger.debug('将数据写入缓存')
        rds.set(key, profile)

    return render_json(profile.to_dict())


def update_profile(request):
    '''修改资料'''
    user_form = UserForm(request.POST)
    profile_form = ProfileForm(request.POST)

    if user_form.is_valid() and profile_form.is_valid():
        uid = request.session['uid']
        # update `user` set nickname='xxx' ... where id = 123;
        User.objects.filter(id=uid).update(**user_form.cleaned_data)
        Profile.objects.update_or_create(id=uid, defaults=profile_form.cleaned_data)

        # 清除旧缓存
        key = keys.PROFILE_K % uid
        rds.delete(key)
        return render_json()
    else:
        err = {}
        err.update(user_form.errors)
        err.update(profile_form.errors)
        raise stat.ProfileErr(err)


def qn_token(request):
    '''获取头像上传凭证'''
    key = 'Avatar-%s' % request.uid  # 上传后的文件名
    token = qn_cloud.get_token(request.uid, key)
    return render_json({'key': key, 'token': token})


def qn_callback(request):
    '''七牛云通知回调'''
    uid = request.POST.get('uid')
    key = request.POST.get('key')

    avatar_url = '%s/%s' % (cfg.QN_HOST, key)
    User.objects.filter(id=uid).update(avatar=avatar_url)
    return render_json(avatar_url)
