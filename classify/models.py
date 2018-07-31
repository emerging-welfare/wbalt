from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import JSONField
from django.db import models
from sqlite3 import *
from django.db import connections
from django.contrib.auth.models import User
import json
import django.contrib.postgres.fields.jsonb
# Create your models here.

class TextFile(models.Model):
    data = {'user': False, 'newuser': False}

    filename = models.CharField(default="", max_length=1000)
    text = models.TextField()
    info = JSONField(default=data)
    def __str__(self):
        return self.text+''