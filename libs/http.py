from django.conf import settings
from django.http import JsonResponse


def render_json(code=0,data=None):
    '''

    :param code:
    :param data:
    :return:
    '''

    result = {
        'code':code
    }
    if data:
        result['data'] = data

    if settings.DEBUG:
        json_dumps_params={'indent':4,'ensure_ascii':False}
    else:
        json_dumps_params={'separators':(',',':')}


    return JsonResponse(result,json_dumps_params=json_dumps_params)
