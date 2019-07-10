import os
import time
from urllib.parse import urljoin

from django.conf import settings
from django.core.cache import cache
from django.http import JsonResponse

from common import utils, errors, config
from libs.http import render_json
from user import logic
from user.forms import ProfileForm
from user.models import User, Profile


def verify_phone(request):
    """
    验证手机号
    :param request:
    :return:
    """
    phone_num = request.POST.get('phone_num', '')
    phone_num = phone_num.strip()

    if utils.is_phone_num(phone_num):
        if logic.send_verify_code(phone_num):
            return render_json()
        else:
            return render_json(code=errors.SmsSendError.code)

    return render_json(code=errors.PhoneNumError.code)


def login(request):
    phone_num = request.POST.get('phone_num', '')
    code = request.POST.get('code', '')

    phone_num = phone_num.strip()
    code = code.strip()

    # 1、检查 验证码
    cached_code = cache.get(config.VERIFY_CODE_CACHE_PREFIX % phone_num)
    if cached_code != code:
        return render_json(code=errors.VerifyCodeError.code)

    # 2、登录或注册
    # try:
    #     user = User.objects.get(phonenum=phone)
    # except User.DoesNotExist:
    #     user = User.objects.create(phonenum=phone)
    #     # 创建用户的同时，使用 user.id 创建 Profile 对象，建立一对一的关联
    #     Profile.objects.create(id=user.id)

    user, created = User.objects.get_or_create(phonenum=phone_num)
    request.session['uid'] = user.id

    return render_json(data=user.to_dict())


def get_profile(request):
    profile = request.user.profile
    return render_json(data=profile.to_dict(exclude=['vibration', 'only_matche', 'auto_play']))


def set_profile(request):
    user = request.user

    form = ProfileForm(request.POST, instance=user.profile)

    if form.is_valid():
        form.save()
        return render_json()
    else:
        return render_json(data=form.errors)


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
        return render_json(code=errors.AvatarUploadError.code)
