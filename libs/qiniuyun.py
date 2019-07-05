from urllib.parse import urljoin

from qiniu import Auth, put_data, put_file

#云库存储图片
from common import config


def upload(filename, filepath):
    # 构建鉴权对象
    qn_auth = Auth(config.QN_ACCESS_KEY, config.QN_SECRET_KEY)

    # 生成上传 Token，可以指定过期时间等
    token = qn_auth.upload_token(config.QN_BUCKET, filename, 3600)

    ret, info = put_file(token, filename, filepath)
    return ret, info
