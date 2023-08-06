# -*- coding=utf-8 -*-


import django
import os

os.environ['DJANGO_SETTINGS_MODULE'] = 'web.settings'
django.setup()
from hammer.django_bulk.helper import bulk_insert

datas = [
    {'one': '123',
     'func': '123'},
    {'one': '456',
     'fuddnc': '123'},
]

bulk_insert('test', datas)
