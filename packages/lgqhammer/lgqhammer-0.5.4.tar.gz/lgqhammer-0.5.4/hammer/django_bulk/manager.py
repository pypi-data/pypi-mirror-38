from django.db import models
from .query import BulkInsertQuerySet


class BulkInsertManager(models.Manager.from_queryset(BulkInsertQuerySet)):
    pass
