from config.default import *

# SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(os.path.join(BASE_DIR, 'board.db'))

SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(
    user='dbmasteruser',
    pw='Q5):6]XysspR:s2sd8K{cPfy2cs$j^=t',
    url='ls-c28b2f5e227541ecbd2a5c9b93ca9a2b7945b52f.cyx36eaqiwou.ap-northeast-2.rds.amazonaws.com',
    db='moveboard')

SQLALCHEMY_TRACK_MODIFICATIONS = False

SECRET_KEY = b'Zb3\x81\xdb\xf1\xd9\xd7-Knb\x8eB\xa5\x18'