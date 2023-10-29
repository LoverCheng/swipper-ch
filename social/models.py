from django.db import models
from django.db.models import Q

from user.models import User


class Swiped(models.Model):
    '''滑动记录'''
    STYPES = (
        ('like', '喜欢'),
        ('superlike', '超级喜欢'),
        ('dislike', '不喜欢'),
    )
    uid = models.IntegerField(verbose_name='滑动者的 UID')
    sid = models.IntegerField(verbose_name='被滑动者的 UID')
    stype = models.CharField(max_length=10, choices=STYPES, verbose_name='滑动类型')
    stime = models.DateTimeField(auto_now_add=True, verbose_name='滑动时间')

    class Meta:
        unique_together = ('uid', 'sid')  # uid 和 sid 联合唯一

    @classmethod
    def is_liked(cls, uid, sid):
        '''检查是否喜欢过某人'''
        stypes = ['like', 'superlike']
        try:
            swipe_record = cls.objects.get(uid=uid, sid=sid)
        except cls.DoesNotExist:
            return None  # 尚未滑动过对方
        else:
            return swipe_record.stype in stypes  # 为 True 说明喜欢，为 False 说明不喜欢


class Friend(models.Model):
    '''好友关系表'''
    uid1 = models.IntegerField()
    uid2 = models.IntegerField()

    class Meta:
        unique_together = ('uid1', 'uid2')  # uid1 和 uid2 联合唯一

    @classmethod
    def make_friends(cls, uid1, uid2):
        '''建立好友关系'''
        uid1, uid2 = sorted([uid1, uid2])  # 将 uid 小的值放到前面
        frd_relation, _ = cls.objects.get_or_create(uid1=uid1, uid2=uid2)
        return frd_relation

    @classmethod
    def is_friends(cls, uid1, uid2):
        '''检查两个人是否是好友关系'''
        uid1, uid2 = sorted([uid1, uid2])  # 将 uid 小的值放到前面
        return cls.objects.filter(uid1=uid1, uid2=uid2).exists()

    @classmethod
    def my_friends(cls, uid):
        '''我所有好友的 ID 列表'''
        frd_id_list = []
        condition = Q(uid1=uid) | Q(uid2=uid)
        for frd in cls.objects.filter(condition):
            if frd.uid1 == uid:
                frd_id_list.append(frd.uid2)
            else:
                frd_id_list.append(frd.uid1)

        return User.objects.filter(id__in=frd_id_list)

    @classmethod
    def break_off(cls, uid1, uid2):
        uid1, uid2 = sorted([uid1, uid2])  # 将 uid 小的值放到前面
        cls.objects.filter(uid1=uid1, uid2=uid2).delete()
