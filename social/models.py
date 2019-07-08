from django.db import models

# Create your models here.
from common import errors
from common.errors import LogicException


class Swiped(models.Model):

    MARKS = (
        ('like', '喜欢'),
        ('dislike', '不喜欢'),
        ('superlike', '超级喜欢')
    )

    uid = models.IntegerField()
    sid = models.IntegerField()
    mark = models.CharField(max_length=16, choices=MARKS)
    created_at = models.DateTimeField(auto_now_add=True)

    @classmethod
    def is_liked(cls,sid,uid):
        return cls.objects.filter(uid=sid,sid=uid,mark__in=['like','superlike']).exists()

    @classmethod
    def swipe(cls,uid,sid,mark):
        makrs=[m for m,_ in cls.MARKS]
        if mark not in makrs:
            raise LogicException(errors.SWIPE_ERR)
        if cls.objects.filter(uid=uid,sid=sid).exists():
            return False
        else:
            cls.objects.create(uid=uid,sid=sid,mark=mark)
            return True

    class Meta:
        db_table = 'swiped'

class FriendManager(models.Manager):
    '''
    自定义manager 扩充models.Manager的默认行为 增加业务相关的方法
    '''
    def make_frinends(self,uid1,uid2):
        uid1,uid2=(uid1,uid2) if uid1<=uid2 else (uid2,uid1)
        # self.create(uid1=uid1, uid2=uid2)
        self.get_or_create(uid1=uid1, uid2=uid2)


class Friend(models.Model):
    '''
    好友关系
    uid fid

    '''
    object=FriendManager()
    uid1=models.IntegerField()
    uid2=models.IntegerField()

    @classmethod
    def make_frinends(cls,uid1,uid2):
        '''
        通过自定义uid顺序的规则来实现好友记录的保存，保证同一组好友关系，只存在一份数据
        :param uid1:
        :param uid2:
        :return:
        '''
        uid1,uid2=(uid1,uid2) if uid1<=uid2 else (uid2,uid1)
        cls.objects.create(uid1=uid1,uid2=uid2)

    @classmethod
    def cancel_friends(cls,uid1,uid2):
        '''

        :param uid1:
        :param uid2:
        :return:
        '''
        uid1,uid2=(uid1,uid2) if uid1<uid2 else (uid2,uid1)
        cls.objects.filter(uid1=uid1, uid2=uid2).delete()

    class Meta:
        db_table='friends'