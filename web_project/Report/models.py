from django.db import models
from User.models import HUser


class RepPost(models.Model):
    rep_target = models.CharField(max_length=30)
    rep_content = models.TextField(max_length=1000)
    rep_date = models.DateTimeField('time')
    rep_author = models.ForeignKey('User.HUser', related_name='rep_s', on_delete=models.CASCADE)

# Create your models here.
