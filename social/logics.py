import datetime

from django.db.transaction import atomic
from django.db.utils import IntegrityError

from swiper import config
from common import keys
from common import stat
from libs.cache import rds
from user.models import User
from user.models import Profile
from social.models import Swiped
from social.models import Friend


def rcmd_from_queue(uid):
    '''从优先推荐队列里面获取用户'''
    key = keys.FIRST_RCMD_Q % uid
    uid_list = rds.lrange(key, 0, 19)  # 从 Redis 取出优先推荐的用户 ID
    uid_list = [int(r_uid) for r_uid in uid_list]  # 将 uid 列表元素强转成 int 类型
    return User.objects.filter(id__in=uid_list)


def rcmd_from_db(uid, num=20):
    '''从数据库获取推荐用户'''
    my_profile = Profile.objects.get(id=uid)

    today = datetime.date.today()
    earliest_birthday = today - datetime.timedelta(my_profile.max_dating_age * 365)  # 最早出生日期
    latest_birthday = today - datetime.timedelta(my_profile.min_dating_age * 365)    # 最晚出生日期

    # 取出已经划过的人的 id
    # select sid from swiped where uid = 1002
    sid_list = Swiped.objects.filter(uid=uid).values_list('sid', flat=True)

    users = User.objects.filter(
        location=my_profile.dating_location,
        gender=my_profile.dating_gender,
        birthday__gte=earliest_birthday,
        birthday__lte=latest_birthday,
    ).exclude(id__in=sid_list)[:num]  # 懒加载

    return users


def rcmd(uid):
    '''推荐滑动用户'''
    q_users = rcmd_from_queue(uid)  # 从优先推荐队列获取用户
    remain = 20 - len(q_users)
    if remain > 0:
        db_users = rcmd_from_db(uid, remain)  # 从数据库获取推荐用户
        return set(q_users) | set(db_users)
    else:
        return q_users


def like_someone(uid, sid):
    '''喜欢（右滑）某人'''
    # 在数据库中添加滑动记录
    try:
        Swiped.objects.create(uid=uid, sid=sid, stype='like')
    except IntegrityError:
        # 重复滑动时，直接返回当前用户是否已匹配成好友
        return Friend.is_friends(uid, sid)

    # 强制将对方从自己的优先推荐队列删除
    rds.lrem(keys.FIRST_RCMD_Q % uid, 0, sid)

    # 修改被滑动用户的积分
    score = config.SWIPE_SCORE['like']
    rds.zincrby(keys.HOTRANK_K, score, sid)

    # 检查对方是否喜欢过 (右滑或者上滑) 自己
    if Swiped.is_liked(sid, uid):
        # 双方互相喜欢，匹配成好友
        Friend.make_friends(uid, sid)
        return True
    else:
        return False


def superlike_someone(uid, sid):
    '''超级喜欢 (上滑) 某人'''
    # 在数据库中添加滑动记录
    try:
        Swiped.objects.create(uid=uid, sid=sid, stype='superlike')
    except IntegrityError:
        # 重复滑动时，直接返回当前用户是否已匹配成好友
        return Friend.is_friends(uid, sid)

    # 强制将对方从自己的优先推荐队列删除
    rds.lrem(keys.FIRST_RCMD_Q % uid, 0, sid)

    # 修改被滑动用户的积分
    score = config.SWIPE_SCORE['superlike']
    rds.zincrby(keys.HOTRANK_K, score, sid)

    # 检查对方是否喜欢过 (右滑或者上滑) 自己
    like_status = Swiped.is_liked(sid, uid)
    if like_status is True:
        # 双方互相喜欢，匹配成好友
        Friend.make_friends(uid, sid)
        return True
    elif like_status is False:
        return False
    else:
        # 对方未滑过自己时，将自己的 uid 添加到对方的 “优先推荐列表”
        key = keys.FIRST_RCMD_Q % sid
        rds.rpush(key, uid)
        return False


def dislike_someone(uid, sid):
    '''不喜欢 (左滑) 某人'''
    # 在数据库中添加滑动记录
    try:
        Swiped.objects.create(uid=uid, sid=sid, stype='dislike')
    except IntegrityError:
        pass

    # 强制将对方从自己的优先推荐队列删除
    rds.lrem(keys.FIRST_RCMD_Q % uid, 0, sid)

    # 修改被滑动用户的积分
    score = config.SWIPE_SCORE['dislike']
    rds.zincrby(keys.HOTRANK_K, score, sid)


def find_fans(uid):
    '''查找自己的粉丝 (自己尚未滑过，但是对方喜欢过自己的人)'''
    # 取出自己已滑过的用户 ID 列表
    sid_list = Swiped.objects.filter(uid=uid).values_list('sid', flat=True)

    like_types = ['like', 'superlike']
    fans_id_list = Swiped.objects.filter(sid=uid, stype__in=like_types)\
                                 .exclude(uid__in=sid_list) \
                                 .values_list('uid', flat=True)

    return User.objects.filter(id__in=fans_id_list)


def rewind_last_swipe(uid):
    '''反悔最后一次滑动记录'''
    now = datetime.datetime.now()

    # 检查今天是否已经达到 3 次
    key = 'Rewind-%s-%s' % (uid, now.date())
    rewind_times = rds.get(key, 0)  # 取出当天反悔次数，默认为 0
    if rewind_times >= 3:
        raise stat.RewindLimited

    # 从数据库取出最后一次滑动记录
    latest_swipe = Swiped.objects.filter(uid=uid).latest('stime')

    # 检查滑动记录是否是五分钟之内的
    past_time = now - latest_swipe.stime
    if past_time.seconds > 300:
        raise stat.RewindTimeout

    with atomic():
        # 检查上次滑动记录是否匹配成功，如果匹配成功需要删除好友
        if latest_swipe.stype in ['like', 'superlike']:
            Friend.break_off(uid, latest_swipe.sid)

        # 检查上次滑动是否是超级喜欢，如果是，将自己的 ID 从对方的优先队列删除
        if latest_swipe.stype == 'superlike':
            rds.lrem(keys.FIRST_RCMD_Q % latest_swipe.sid, 0, uid)

        # 撤销被滑动用户的积分
        score = -config.SWIPE_SCORE[latest_swipe.stype]
        rds.zincrby(keys.HOTRANK_K, score, latest_swipe.sid)

        # 删除滑动记录
        latest_swipe.delete()

        # 累加当天反悔次数
        rds.set(key, rewind_times + 1)


def top_n(num):
    '''获取热度排行前 N 的数据'''
    origin_rank = rds.zrevrange('HotRank', 0, num - 1, withscores=True)  # 从redis取出原始排行数据
    cleaned_rank = [[int(uid), int(score)] for uid, score in origin_rank]  # 对原始排名数据进行清洗

    # 取出所有用户
    uid_list = [uid for uid, _ in cleaned_rank]
    users = User.objects.filter(id__in=uid_list)
    # 将 user 按照 uid 在 uid_list 中的索引排序
    users = sorted(users, key=lambda user: uid_list.index(user.id))

    rank_data = []
    exclude_fields = ['phonenum', 'birthday', 'location', 'vip_id', 'vip_end']
    for index, (_, score) in enumerate(cleaned_rank):
        user = users[index]
        user_info = user.to_dict(exclude_fields)
        user_info['rank'] = index + 1
        user_info['score'] = score
        rank_data.append(user_info)

    return rank_data
