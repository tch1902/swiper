'''
业务模块配置
'''


# 云之讯短信平台配置
YZX_SMS_URL = 'https://open.ucpaas.com/ol/sms/sendsms'

YZX_SMS_PARAMS = {
    'sid':'bc2595d7eee20ccc2a5d16ab04437f65',
    'token':'cc1108c6c4a0a0f31fb56b9c21d4d370',
    'appid':'c16ea9ea865b42dfba7d90c1dca3338b',
    'templateid':'482027',
    'param':None,
    'mobile':None

}

#缓存 key prefix
VERIFY_CODE_CACHE_PREFIX='verfiy_code:%s'
REWIND_CACHE_PREFIX='rewind:%s'

#七牛云配置
ACCESS_KEY = 'Iti8rKoa9Ey3rOJlGgz0zaCT58kvqN47Qy2m6jh6'
SECRET_KEY = 'Lju4wCmZe52Zkp3sgFTqgx_QSy9MKsws36uWVeMV'
# 要上传的空间
BUCKET_NAME = 'myblog'
HOST='http://www.chenyyuan.com'

#用户每天撤销次数
REWIND_TIMES=3

