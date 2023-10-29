import os
import sys
import json

from django.test import TestCase
from django.conf import settings

scripts_dir = os.path.join(settings.BASE_DIR, 'scripts')
sys.path.append(scripts_dir)

from data_init import create_robots
from data_init import create_vip_data
from user.models import User
from common.keys import VCODE_K
from libs.cache import rds


class UserTest(TestCase):
    def setUp(self):
        super().setUp()
        create_robots(1000)
        create_vip_data()
        rds.set(VCODE_K % '15601185621', '123456')  # 在 Redis 中缓存验证码
        user = User.objects.create(id=1001, nickname='Seamile', phonenum='15601185621')

    def test_login(self):
        response = self.client.post('/api/user/vcode/submit',
                                    {'phonenum': '15601185621', 'vcode': '123456'})
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.content)
        self.assertEqual(result.get('data', {}).get('id'), 1001)
        self.assertEqual(result.get('data', {}).get('phonenum'), '15601185621')

    def test_like(self):
        # 先登录
        self.client.post('/api/user/vcode/submit',
                                    {'phonenum': '15601185621', 'vcode': '123456'})

        response = self.client.post('/api/social/like', data={'sid': '100'})
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.content)
        self.assertEqual(result.get('code'), 0)
