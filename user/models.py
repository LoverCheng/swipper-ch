import datetime

from django.db import models

from vip.models import Vip


class User(models.Model):
    '''用户'''
    GENDERS = (
        ('male', '男性'),
        ('female', '女性'),
    )
    LOCATIONS = (
        ('北京', '北京'),
        ('上海', '上海'),
        ('深圳', '深圳'),
        ('武汉', '武汉'),
        ('成都', '成都'),
        ('西安', '西安'),
        ('沈阳', '沈阳'),
    )
    phonenum = models.CharField(max_length=16, unique=True, verbose_name='手机号')
    nickname = models.CharField(max_length=20, db_index=True, verbose_name='昵称')
    gender = models.CharField(max_length=10, choices=GENDERS, default='male', verbose_name='性别')
    birthday = models.DateField(default='2000-01-01', verbose_name='出生日')
    avatar = models.CharField(max_length=256, verbose_name='个人形象 URL')
    location = models.CharField(max_length=10, default='上海', choices=LOCATIONS, verbose_name='常居地')

    vip_id = models.IntegerField(default=1, verbose_name='用户的 VIP ID')
    vip_end = models.DateTimeField(default='3000-01-01', verbose_name='VIP截止日期')

    @property
    def profile(self):
        if not hasattr(self, '_profile'):
            self._profile, _ = Profile.objects.get_or_create(id=self.id)
        return self._profile

    @property
    def vip(self):
        '''用户的 VIP数据'''
        now = datetime.datetime.now()
        if now >= self.vip_end:
            self.set_vip(1)

        if not hasattr(self, '_vip'):
            self._vip = Vip.objects.get(id=self.vip_id)
        return self._vip

    def set_vip(self, vip_id):
        '''设置用户的VIP'''
        self._vip = Vip.objects.get(id=vip_id)
        self.vip_id = vip_id
        self.vip_end = datetime.datetime.now() + datetime.timedelta(self._vip.duration)
        self.save()


class Profile(models.Model):
    '''用户交友资料'''
    dating_location = models.CharField(max_length=10, default='上海', choices=User.LOCATIONS,
                                       verbose_name='目标城市')
    dating_gender = models.CharField(max_length=10, choices=User.GENDERS, default='female',
                                     verbose_name='匹配的性别')

    min_distance = models.FloatField(default=1.0, verbose_name='最小查找范围')
    max_distance = models.FloatField(default=10.0, verbose_name='最大查找范围')
    min_dating_age = models.IntegerField(default=18, verbose_name='最小交友年龄')
    max_dating_age = models.IntegerField(default=50, verbose_name='最大交友年龄')

    vibration = models.BooleanField(default=True, verbose_name='是否开启震动')
    only_matched = models.BooleanField(default=True, verbose_name='不让陌生人看我的相册')
    auto_play = models.BooleanField(default=True, verbose_name='自动播放视频')
