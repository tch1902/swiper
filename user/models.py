import datetime

from django.db import models

# Create your models here.

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
    phonenum = models.CharField(max_length=11,unique=True)
    nickname = models.CharField(max_length=32)
    sex = models.CharField(default=0,max_length=100)
    birth_year = models.IntegerField(default=2000)
    birth_mohth = models.IntegerField(default=1)
    birth_day = models.IntegerField(default=1)
    avatar = models.CharField(max_length=256)
    location = models.CharField(max_length=64)

    @property   #声明成user对象的属性
    def age(self):
        today=datetime.date.today()
        birthday=datetime.date(self.birth_year,self.birth_mohth,self.birth_day)
        return (today-birthday).days//365


    def to_dict(self):
        return {'uid':self.id,'phonenum':self.phonenum,
                'nickname':self.nickname,
                'sex':self.sex,
                'age':self.age}


    class Meta:
        db_table = "users"