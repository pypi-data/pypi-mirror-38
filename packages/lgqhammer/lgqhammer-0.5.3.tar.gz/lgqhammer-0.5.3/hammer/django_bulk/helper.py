# -*- coding=utf-8 -*-
from django.db import models

from .manager import BulkInsertManager
from .models import Virtual


def bulk_create(objs, meta=None, batch_size=None):
    assert batch_size is None or batch_size > 0
    if not objs:
        return
    objs = list(objs)
    if meta is None:
        meta = objs[0]._meta
    meta.model.objects = BulkInsertManager()
    meta.model.objects.model = meta.model
    meta.model.objects.bulk_create(objs)


# db_table 存储的表名
# datas 存储的数据列表，默认取第一个数据的 keys
def bulk_insert(db_table, datas=[]):
    if not datas:
        return

    objs = []
    for i, data in enumerate(datas):
        obj = Virtual()
        obj._meta.db_table = db_table
        for key, value in data.items():
            m = models.TextField(default=None)
            m.column = key
            m.attname = key
            m.name = key
            m.value = value
            setattr(obj, key, value)
            if i == 0:
                obj._meta.local_fields.append(m)

        if i == 0:
            obj._meta.concrete_fields = obj._meta.local_fields
        objs.append(obj)
    bulk_create(objs)


def bulk_create_or_update(objs, meta=None, update_fields=None, exclude_fields=None,
                          using='default', batch_size=None, pk_field='pk'):
    pass
