import os
import time

from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.shortcuts import render


# Create your views here.
from common import utils, errors, config

from libs.http import render_json
from swiper import settings
from user import logic
from user.forms import ProfileForm
from user.models import User, Profile


def verify_phone(request):
    '''
    验证手机好
    :param request:
    :return:
    '''
    phone_num = request.POST.get('phone_num')

    if utils.is_phone_num(phone_num.strip()):
        if logic.send_verify_code(phone_num):
            return render_json()
        else:
            return render_json(code=errors.SMS_SEND_ERR)

    return render_json(code=errors.PHONE_NUM_ERR)


def login(request):
    phone_num = request.POST.get('phone_num')
    code = request.POST.get('code')

    phone_num=phone_num.strip()
    code=code.strip()

    #1.检查 验证码
    cache_code = cache.get(config.VERIFY_CODE_CACHE_PREFIX % phone_num)
    print(' ------',cache_code,code)
    if cache_code!=code:
        return render_json(code=errors.VERIFY_CODE_ERR)

    #2.登陆 注册
    # try:
    #     user = User.objects.get(phonenum=phone)
    # except User.DoesNotExist:
    #     user = User.objects.create(phonenum=phone)
    #     # 创建用户的同时，使用 user.id 创建 Profile 对象，建立一对一的关联
    #     Profile.objects.create(id=user.id)

    user,create=User.objects.get_or_create(phonenum=phone_num)
    request.session['uid']=user.id

    return render_json(data=user.to_dict())

#个人信息
def get_profile(request):
    # uid=request.GET.get('uid')
    # user=User.objects.get(id=uid)
    # profile=Profile.objects.get(id=uid)
    profile=request.user.profile
    return render_json(data=profile.to_dict(exclude=['vibration','only_matche','auto_play']))


def set_profile(request):
    user=request.user
    form=ProfileForm(request.POST,instance=user.profile)
    # form=ProfileForm(request.POST)
    if form.is_valid():
        # profile=form.save(commit=False)
        #手动创建 一对一 关系
        # profile.id=user.id
        form.save()

        return render_json()
    else:
        return render_json(data=form.errors)

#保存到本地
def upload_profile1(request):
    avatar=request.FILES.get('avatar')
    user=request.user
    filename='avatar-%s-%d'%(user.id,int(time.time()))
    filepath=os.path.join(settings.MEDIA_ROOT,filename)

    #wb:二进制写入，wb+：可读可写
    with open(filepath,'wb+') as output:
        for chunk in avatar.chunks():
            output.write(chunk)

    user.avatar=filename
    user.save()

    return render_json(data=user.avatar)

#异步
def upload_avatar(request):
    avatar = request.FILES.get('avatar')
    user = request.user

    # filename = 'avatar-%s-%d' % (user.id, int(time.time()))
    # filepath = os.path.join(settings.MEDIA_ROOT, filename)
    #
    # with open(filepath, 'wb+') as output:
    #     for chunk in avatar.chunks():
    #         output.write(chunk)

    ret = logic.async_upload_avatar(user, avatar)

    if ret:
        return render_json()
    else:
        return render_json(code=errors.AVATAR_UPLOAD_ERR)
