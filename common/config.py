"""
业务模块配置
"""
# 缓存 key prefix
VERIFY_CODE_CACHE_PREFIX = 'verfiy_code:%s'
REWIND_CACHE_PREFIX = 'rewind:%s'
PROFILE_DATA_CACHE_PREFIX = 'profile_data:%s'
MODEL_CACHE_PREFIX = 'model:%s:%s'
HOT_RANK_KEY = 'hot_rank'

# 社交模块配置
REWIND_TIMES = 3

SWIPE_SCORES={
    'like':5,
    'superlike':8,
    'dislike':0
}

# 云之讯短信平台配置
YZX_SMS_URL = 'https://open.ucpaas.com/ol/sms/sendsms'

YZX_SMS_PARAMS = {
    'sid': '22ac8d51a958dc580d8503173199845c',
    'token': '8f44a2423cba9bf316d6197e88bfd3ac',
    'appid': '14595d89fddf4bbfa633f497a673a0b8',
    'templateid': '481679',
    'param': None,
    'mobile': None
}

# 七牛云配置
QN_ACCESS_KEY = 'ktgbAUqxq6D2WZ0PXRhRY4s5TvW2W_NcpuspuhcG'
QN_SECRET_KEY = 'XmsJZNH9LgCySF667ZtF-QZI1P6iI2tZXTwZw9ea'
QN_BUCKET = 'swiper'
QN_HOST = 'http://pu420clqe.bkt.clouddn.com'
