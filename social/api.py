from django.shortcuts import render

# Create your views here.
from common import errors
from libs.http import render_json
from social import logic
from social.models import Swiped
from user.models import User


def recommend(request):
    '''
    根据当前登陆用户
    :param request:
    :return:
    '''
    recm_users=logic.recommend_users(request.user)
    print(recm_users)
    users=[u.to_dict() for u in recm_users]
    print(users)
    return render_json(data=users)


def like(request):
    print(request.POST.get('sid'),type(request.POST.get('sid')))
    sid=int(request.POST.get('sid'))
    user=request.user

    matched=logic.like_someone(user.id,sid)
    return render_json(data={'matched':matched})
    # if logic.like_someone(user.id,sid):
    #     return render_json()
    # else:
    #     return render_json(errors)

def superlike(request):
    sid = int(request.POST.get('sid'))
    user = request.user

    matched = logic.superlike_someone(user.id, sid)
    return render_json(data={'matched': matched})

    # if logic.superlike_someone(user.id, sid):
    #     return render_json()
    # else:
    #     return render_json(errors)

def dislike(request):
    sid = int(request.POST.get('sid'))
    user = request.user

    Swiped.swipe(uid=user.id,sid=sid,mark='dislike')
    return render_json()

def rewind(request):
    '''
    反悔
    不需要从客户端
    :param request:
    :return:
    '''
    logic.rewind(request.user)

    return None


def liked_me(request):
    '''
    喜欢我的人列表
    :param request:
    :return:
    '''
    liked_me_uids_list=logic.likeme(request.user)
    users=User.objects.filter(id__in=liked_me_uids_list)
    user_list=[u.to_dict() for u in users]
    return render_json(data=user_list)

def friends(request):
    friends=logic.friends(request.user)
    users = User.objects.filter(id__in=friends)
    user_list = [u.to_dict() for u in users]
    return render_json(data=user_list)