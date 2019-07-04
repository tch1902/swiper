from django.core.cache import cache
from django.shortcuts import render


# Create your views here.
from common import utils, errors, config
from libs.http import render_json
from user import logic
from user.models import User


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
    user,create=User.objects.get_or_create(phonenum=phone_num)
    request.session['uid']=user.id

    return render_json(data=user.to_dict())



