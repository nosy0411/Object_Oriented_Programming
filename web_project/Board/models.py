from django.db import models
# 장고 기본 유저 정보를 가져옴
from django.conf import settings


# Create your models here.
class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='my_post', on_delete=models.CASCADE)
    content = models.CharField(max_length=100)
    date = models.DateTimeField('time')
    state = models.CharField(max_length=20)
    page = models.IntegerField(default=0)

    def __str__(self):
        return str(self.author) + ' ' + self.content
