import datetime

from django.core.cache import cache
from django.db.models import Q

from common import config, errors
from social.models import Swiped, Friend
from user.models import User


def recommend_users(user):
    '''
    筛选符合user.profile条件的用户
    过滤掉已经被划过的用户
    :param user:
    :return:
    '''
    today=datetime.date.today()

    #1999=2019-20
    max_year=today.year-user.profile.min_dating_age
    #2001=2019-18
    min_year=today.year-user.profile.max_dating_age

    #only 只取一个字段，节省流量
    swiped_users=Swiped.objects.filter(uid=user.id).only('sid')
    swiped_sid_list=[s.sid for s in swiped_users]

    users=User.objects.filter(
        sex=user.profile.dating_sex,
        location=user.profile.location,
        birth_year__gte=min_year,
        birth_year__lte=max_year,

    ).exclude(id__in=swiped_sid_list)[:20]

    # print(users.query)
    return users

def like_someone(uid,sid):
    '''
    创建喜欢的人，如果对方也喜欢，则建立好友关系
    :param uid:
    :param sid:
    :return:
    '''

    if not User.objects.filter(id=sid):
        return False

    #创建滑动记录
    # Swiped.objects.create(uid=uid,sid=sid,mark='like')
    ret=Swiped.swipe(uid=uid,sid=sid,mark='like')

    #只有滑动成功，才进行好友匹配
    #如果被滑动的人喜欢过我，建立好友关系
    if ret and Swiped.is_liked(sid,uid):
        #TODO:向sid用户发送推送通知
        Friend.object.make_frinends(uid,sid)

    return ret

def superlike_someone(uid,sid):
    '''
    创建喜欢的人，如果对方也喜欢，则建立好友关系
    :param uid:
    :param sid:
    :return:
    '''

    if not User.objects.filter(id=sid):
        return False

    #创建滑动记录
    # Swiped.objects.create(uid=uid,sid=sid,mark='superlike')
    Swiped.swipe(uid=uid,sid=sid,mark='superlike')

    if Swiped.is_liked(sid,uid):
        Friend.make_frinends(uid,sid)

    return True

def rewind(user):
    '''
    撤销当前登陆用户的上一次操作
    每天只能撤销3次
    :param user:
    :return:
    '''
    key=config.REWIND_CACHE_PREFIX%user.id
    rewind_times=cache.get(key,0)
    if rewind_times>=config.REWIND_TIMES:
        raise errors.RewindLimitError

    swipe=Swiped.objects.filter(uid=user.id).latest('created_at')

    if swipe.mark in ['like','superlike']:
        Friend.cancel_friends(user.id,swipe.id)

    swipe.delete()

    now=datetime.datetime.now()
    timeout=86400-now.hour-now.minute-now.second
    cache.set(key,rewind_times+1,timeout=timeout)

def likeme(user):
    '''
    喜欢我的人的列表
    :param user:
    :return:
    '''
    swipe_list=Swiped.objects.filter(sid=user.id,mark__in=['like','superlike'])
    liked_me_uids_list = [s.uid for s in swipe_list]
    #过滤掉已经加为好友的用户
    #TODO：获取好友列表
    friends_list=Friend.object.filter(Q(uid1=user.id)|Q(uid2=user.id))
    friends_uids_list = [f.uid1 for f in friends_list]
    friends_uids_list +=[f.uid2 for f in friends_list]
    friends_uids_list=list(set(friends_uids_list))
    for f in friends_uids_list:
        if f in liked_me_uids_list:
            liked_me_uids_list.remove(f)

    print(liked_me_uids_list,friends_uids_list)
    return liked_me_uids_list

def friends(user):
    friends_list = Friend.object.filter(Q(uid1=user.id) | Q(uid2=user.id))
    friends_uids_list = [f.uid1 for f in friends_list]
    friends_uids_list += [f.uid2 for f in friends_list]
    friends_uids_list = list(set(friends_uids_list))
    friends_uids_list.remove(user.id)
    return friends_uids_list
