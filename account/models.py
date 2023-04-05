from django.db import models
from django.contrib.auth.models import AbstractUser

LANG_CHOICES = (
    ('uz', "O'zbek"),
    ('ru', "Русский"),
)


class User(AbstractUser):
    first_name = models.CharField(max_length=150, blank=True, null=True)
    last_name = models.CharField(max_length=150, blank=True, null=True)
    complete = models.IntegerField(default=0)
    birth_date = models.DateField(default=None, null=True, blank=True)
    chat_id = models.BigIntegerField(default=0)
    group_id = models.CharField(max_length=40, null=True, blank=True)
    notification = models.BooleanField(default=False)
    language = models.CharField(choices=LANG_CHOICES, max_length=50, null=True, blank=True)

    def __str__(self):
        return self.username



