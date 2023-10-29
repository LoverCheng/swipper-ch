import logging

from libs.http import render_json
from social import logics
from social.models import Friend
from vip.logics import require_perm

inf_logger = logging.getLogger('inf')


def rcmd_users(request):
    '''推荐用户'''
    users = logics.rcmd(request.uid)
    result = [user.to_dict() for user in users]
    return render_json(result)


def like(request):
    '''喜欢'''
    sid = int(request.POST.get('sid'))
    is_matched = logics.like_someone(request.uid, sid)
    inf_logger.info(f'{request.uid} like {sid}')
    return render_json({'is_matched': is_matched})


@require_perm('superlike')
def superlike(request):
    '''超级喜欢'''
    sid = int(request.POST.get('sid'))
    is_matched = logics.superlike_someone(request.uid, sid)
    inf_logger.info(f'{request.uid} superlike {sid}')
    return render_json({'is_matched': is_matched})


def dislike(request):
    '''不喜欢'''
    sid = int(request.POST.get('sid'))
    logics.dislike_someone(request.uid, sid)
    inf_logger.info(f'{request.uid} dislike {sid}')
    return render_json()


@require_perm('rewind')
def rewind(request):
    '''反悔'''
    logics.rewind_last_swipe(request.uid)
    return render_json()


@require_perm('show_fans')
def show_fans(request):
    '''查看粉丝'''
    fans = logics.find_fans(request.uid)
    result = [user.to_dict() for user in fans]
    return render_json(result)


def show_friends(request):
    '''查看好友'''
    friends = Friend.my_friends(request.uid)
    result = [frd.to_dict() for frd in friends]
    return render_json(result)


def hot_rank(request):
    '''热度排名'''
    rank_data = logics.top_n(50)
    return render_json(rank_data)
