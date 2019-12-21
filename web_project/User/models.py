from django.db import models
# 장고 기본 유저 정보를 가져옴
from django.conf import settings


class HUser(models.Model):             # 유저 핸들. 최소의 정보만 담기
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='handle')
    name = models.CharField(max_length=20)
    skku = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Worked(models.Model):
    student = models.ForeignKey('HUser', related_name='worked_s', on_delete=models.CASCADE)
    teacher = models.ForeignKey('HUser', related_name='worked_t', on_delete=models.CASCADE)


class Line(models.Model):               # 인스턴스 하나=메시지 1개
    student = models.ForeignKey('HUser', related_name='line_s', on_delete=models.CASCADE)
    teacher = models.ForeignKey('HUser', related_name='line_t', on_delete=models.CASCADE)
    alive = models.BooleanField()
    date = models.DateTimeField()
    content = models.CharField(max_length=200)


class Eval(models.Model):
    teacher = models.ForeignKey('HUser', related_name='rating', on_delete=models.CASCADE)
    score = models.IntegerField()       # 1~5점
    details = models.CharField(max_length=40, default='')
    student = models.ForeignKey('HUser', related_name='my_eval', on_delete=models.CASCADE, default=None)

class Profile(models.Model):
    target = models.OneToOneField('HUser', on_delete=models.CASCADE)
    is_male = models.BooleanField(default=True)
    age = models.IntegerField(default=0)
    intro = models.CharField(max_length=40, default='안녕')
    subj = models.CharField(max_length=80,default='')
    region = models.CharField(max_length=80,default='')
    score = models.FloatField(default=0)
    exp = models.IntegerField(default=0)
    dep = models.CharField(max_length=40, default='과')

    def score_update(self):
        self.exp = self.target.rating.all().count()
        if self.exp == 0:
            self.score = 0
            self.save()
            return
        s = 0
        for a in self.target.rating.all():
            s += a.score
        s /= self.exp
        self.score = s
        self.save()
