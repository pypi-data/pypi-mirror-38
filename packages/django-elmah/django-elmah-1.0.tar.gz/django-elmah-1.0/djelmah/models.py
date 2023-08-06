from django.db import models

class DjelmahHost(models.Model):
    hostname = models.CharField(max_length=256)
    username = models.CharField(max_length=150)
    api_key = models.CharField(max_length=128)
    active = models.BooleanField(default=True)

class DjelmahLog(models.Model):
    host = models.CharField(max_length=128)
    path = models.CharField(max_length=2048)
    username = models.CharField(max_length=32)
    datetime = models.DateTimeField()
    error_type = models.CharField(max_length=64)
    error_message = models.TextField(blank=True)
    status_code = models.CharField(max_length=8, blank=True)
    raw_html = models.TextField(blank=True)
