from django.db import models
from django.contrib.postgres.fields import JSONField

class Case:
    name = models.CharField(max_length=100, db_index=True)
    recap_id = models.IntegerField()
    pacer_id = models.CharField(db_index=True)
    date_filed = models.DateField(db_index=True)
    date_terminated = models.DateField(db_index=True, blank=True, null=True)
    date_blocked = models.DateField(db_index=True, blank=True, null=True)
    jurisdiction = models.CharField(max_length=10)
    chapter = models.CharField(
        max_length=10,
        db_index=True,
        blank=True,
        null=True
    )
    data = JSONField()

    def __str__(self):
        return self.name


class DocketEntry:
    recap_id = models.IntegerField()
    date_filed = models.DateField(db_index=True)
    description = models.CharField(blank=True, null=True, max_length=200)
    data = JSONField()

    def __str__(self):
        return self.recap_id


class Document:
    recap_id = models.IntegerField()
    pacer_id = models.IntegerField(db_index=True)
    doc_type = models.CharField(max_length=10)
    is_sealed = models.BooleanField()
    is_available = models.BooleanField()
    file_url = models.URLField(blank=True, null=True, max_length=2048)
    description = models.CharField(blank=True, null=True, max_length=200)
    text = models.CharField(blank=True, null=True)
    data = JSONField()

    def __str__(self):
        return self.pacer_id