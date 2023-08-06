# -*- coding=utf-8 -*-


import django
import os
import sys
import datetime
import random
import time

os.environ['DJANGO_SETTINGS_MODULE'] = 'web.settings'
django.setup()

from web.other.models import BilibiliPlay
from .helper import bulk_create


def test_once_get():
    start = time.time()
    for i in range(0, 1000):
        info = {
            'insert_date': datetime.datetime.today(),
            'season_id': i,
            'pub_time': datetime.datetime.today(),
        }
        BilibiliPlay.objects.get_or_create(season_id=i, insert_date=datetime.datetime.today(), defaults=info)
    print('test_once_get use time:%s' % (time.time() - start))


def test_once_update():
    start = time.time()
    for i in range(1000, 2000):
        info = {
            'insert_date': datetime.datetime.today(),
            'season_id': i,
            'pub_time': datetime.datetime.today(),
        }
        BilibiliPlay.objects.update_or_create(season_id=i, insert_date=datetime.datetime.today(), defaults=info)
    print('test_once_update use time:%s' % (time.time() - start))


def test_default_bulk():
    start = time.time()
    objs = []
    for i in range(2000, 3000):
        info = {
            'insert_date': datetime.datetime.today(),
            'season_id': i,
            'pub_time': datetime.datetime.today(),
        }
        objs.append(BilibiliPlay(**info))

    BilibiliPlay.objects.bulk_create(objs)
    print('test_default use time:%s' % (time.time() - start))


def test_custom_bulk():
    start = time.time()
    objs = []
    for i in range(3000, 4000):
        info = {
            'insert_date': datetime.datetime.today(),
            'season_id': i,
            'pub_time': datetime.datetime.today(),
        }
        objs.append(BilibiliPlay(**info))

    bulk_create(objs)
    print('test_custom use time:%s' % (time.time() - start))


if __name__ == '__main__':
    BilibiliPlay.objects.all().delete()

    # test_once_get()
    # test_once_update()
    # test_default_bulk()
    test_custom_bulk()

'''
'UPDATE `other_bilibili_play` SET `name` = (CASE `id` WHEN %s THEN %s WHEN %s THEN %s WHEN %s THEN %s WHEN %s THEN %s WHEN %s THEN %s ELSE `name` END) WHERE `id` in (%s, %s, %s, %s, %s)'

'''
