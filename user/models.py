import datetime

from django.db import models

# Create your models here.
from django.utils.functional import cached_property

from libs.orm import ModelToDictMixin


class User(models.Model):
    '''
    phonenum    手机号
    nickname     昵称
    sex          性别
    birth_year   出生年
    birth_month  出生月
    birth_day    出生日
    avatar        头像
    location      常居地
    '''
    LOCATIONS = (
        ('bj', '北京'),
        ('sz', '深圳'),
        ('sh', '上海'),
        ('gz','广州'),
        ('cd','成都'),
        ('dl','大连'),
    )

    SEXS = (
        (0, '全部'),
        (1, '男'),
        (2, '女')
    )


    phonenum = models.CharField(max_length=11,unique=True)
    nickname = models.CharField(max_length=32)
    sex = models.CharField(default=0,max_length=100,choices=SEXS)
    birth_year = models.IntegerField(default=2000)
    birth_month = models.IntegerField(default=1)
    birth_day = models.IntegerField(default=1)
    avatar = models.CharField(max_length=256)
    location = models.CharField(max_length=64,choices=LOCATIONS)

    # @property   #声明成user对象的属性
    @cached_property
    def age(self):
        today=datetime.date.today()
        birthday=datetime.date(self.birth_year,self.birth_month,self.birth_day)
        return (today-birthday).days//365

    @property
    def profile(self):
        if not hasattr(self,'_profile'):
            self._profile, _ =Profile.objects.get_or_create(id=self.id)

        return self._profile

    def to_dict(self):
        return {'uid':self.id,'phonenum':self.phonenum,
                'nickname':self.nickname,
                'sex':self.sex,
                'age':self.age}


    class Meta:
        db_table = "users"

class Profile(models.Model,ModelToDictMixin):
    LOCATIONS=(
        ('bj','北京'),
        ('sz','深圳'),
        ('sh','上海'),
        ('gz', '广州'),
        ('cd', '成都'),
        ('dl', '大连'),
    )

    SEXS=(
        (0,'全部'),
        (1,'男'),
        (2,'女')
    )

    location=models.CharField(max_length=64,choices=LOCATIONS)
    min_distance=models.IntegerField(default=1)
    max_distance=models.IntegerField(default=10)
    min_dating_age=models.IntegerField(default=18)
    max_dating_age=models.IntegerField(default=81)
    dating_sex=models.IntegerField(default=0,choices=SEXS)
    vibration=models.BooleanField(default=True)
    only_matche=models.BooleanField(default=True)
    auto_play=models.BooleanField(default=True)

    class Meta:
        db_table = "profile"