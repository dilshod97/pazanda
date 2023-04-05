from django.db import models


class Activity(models.Model):
    chat_id = models.BigIntegerField()
    type = models.CharField(max_length=100, null=True, blank=True)
    detail = models.TextField(null=True, blank=True)
    drug = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
