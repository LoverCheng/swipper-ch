import logging
from datetime import date, datetime

from django.db.models import query
from django.db import models

from common.keys import MODEL_K
from libs.cache import rds

TIMEOUT = 1209600  # 缓存两周
inf_logger = logging.getLogger('inf')


def get(self, *args, **kwargs):
    """
    Perform the query and return a single object matching the given
    keyword arguments.
    """
    cls_name = self.model.__name__  # 取出当前 Model 类的名字

    pk = kwargs.get('pk') or kwargs.get('id')
    if pk:
        # 从 redis 获取 Model 对象
        key = MODEL_K % (cls_name, pk)
        model_obj = rds.get(key)
        # inf_logger.debug(f'从缓存获取对象: {model_obj}')
        if isinstance(model_obj, self.model):
            return model_obj

    # 缓存中如果没有取到，直接从数据库获取
    model_obj = self._get(*args, **kwargs)
    # inf_logger.debug(f'从数据库获取对象: {model_obj}')

    # 将取出的 Model 对象写入缓存
    key = MODEL_K % (cls_name, model_obj.pk)
    rds.set(key, model_obj, TIMEOUT)
    # inf_logger.debug('将 model 对象写入缓存')

    return model_obj


def save(self, force_insert=False, force_update=False, using=None,
         update_fields=None):
    """
    Save the current instance. Override this in a subclass if you want to
    control the saving process.

    The 'force_insert' and 'force_update' parameters can be used to insist
    that the "save" must be an SQL insert or update (or equivalent for
    non-SQL backends), respectively. Normally, they should not be set.
    """
    # 执行 Django 原生 save 方法将数据保存到 Database
    self._save()

    # 将对象保存到 redis
    # inf_logger.debug('将 model 对象写入缓存')
    key = MODEL_K % (self.__class__.__name__, self.pk)
    rds.set(key, self, TIMEOUT)


def to_dict(self, exclude=None):
    '''将 Model 对象的属性封装成一个 dict'''
    attr_dict = {}
    exclude = exclude or []

    for field in self._meta.fields:
        name = field.attname

        if name not in exclude:
            value = getattr(self, name)

            # 检查 value 是否是特殊类型，特殊类型需要强转成字符串
            if isinstance(value, (date, datetime)):
                value = str(value)

            attr_dict[name] = value

    return attr_dict


def patch_model():
    '''通过 Monkey Patch 的方式为 Model 增加缓存处理'''
    query.QuerySet._get = query.QuerySet.get
    query.QuerySet.get = get

    models.Model._save = models.Model.save
    models.Model.save = save

    models.Model.to_dict = to_dict
