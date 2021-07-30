import os
import json
BASE_DIR = os.path.dirname(__file__)

SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(os.path.join(BASE_DIR, 'board.db'))
SQLALCHEMY_TRACK_MODIFICATIONS = False


# SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(
#     user='jyg0172',
#     pw='aa72853572!!',
#     url='moveboard.cl9ylma0ul2x.ap-northeast-2.rds.amazonaws.com',
#     db='moveboard'
# )


# with open(os.path.join(BASE_DIR, 'secret.json'), 'r') as f:
#     secret = json.loads(f.read())
#
#
# def get_secret(setting, secret=secret):
#     try:
#         return secret[setting]
#     except:
#         msg = "Set key '{0}' in secret.json".format(setting)
#
#
# AWS_ACCESS_KEY_ID = get_secret('AWS_ACCESS_KEY_ID')
# AWS_SECRET_ACCESS_KEY = get_secret('AWS_SECRET_ACCESS_KEY')
# AWS_STORAGE_BUCKET_NAME = 'hintphone'