import os
import json
BASE_DIR = os.path.dirname(__file__)

# SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(os.path.join(BASE_DIR, 'board.db'))
# SQLALCHEMY_TRACK_MODIFICATIONS = False

with open(os.path.join(BASE_DIR, 'secret.json'), 'r') as f:
    secret = json.loads(f.read())


def get_secret(setting, secret=secret):
    try:
        return secret[setting]
    except:
        msg = "Set key '{0}' in secret.json".format(setting)


SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(
    user=get_secret('USER'),
    pw=get_secret('PW'),
    url=get_secret('URL'),
    db=get_secret('DB')
)
