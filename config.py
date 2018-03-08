# -*- coding: utf-8 -*-
from datetime import timedelta
import os

VERSION='0.1'
DEBUG=True

# Define the application directory
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

#: Define the database
# SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'app.db')
# DATABASE_CONNECT_OPTIONS = {}


#: HOST
if os.environ.get('PURPOSE') == 'PROD':
    HOST=''
    #SESSION_COOKIE_DOMAIN=".ciceron.me"
    #SESSION_COOKIE_PATH="/"
elif os.environ.get('PURPOSE') == 'DEV':
    HOST=''
    #SESSION_COOKIE_DOMAIN=".ciceron.xyz"
    #SESSION_COOKIE_PATH="/"
else:
    HOST='http://localhost'


#: Session
SESSION_TYPE = 'redis'
SESSION_COOKIE_NAME = "MarocatCiceronCookie"
PERMANENT_SESSION_LIFETIME = timedelta(minutes=30)
SECRET_KEY = os.urandom(24)

#: Swagger
SWAGGER = {
    'title': 'My flask API',
    'uiversion': 2
}

#: SQLAlchemy, DB
#SQLALCHEMY_DATABASE_URI='mysql+pymysql://root:ciceron01!@ciceron.xyz/marocat'
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:ciceron01!@ciceronservice2.cng6yzqtxqhh.ap-northeast-1.rds.amazonaws.com/marocat v1.1'
SQLALCHEMY_TRACK_MODIFICATIONS = True


#: JSON으로 들어온 데이터들을 정렬해준다
JSON_SORT_KEYS=False
MAX_CONTENT_LENGTH=5 * 1024 * 1024
UPLOAD_FOLDER_RESULT="results"


#: Facebook
FACEBOOK_APP_ID = '931700420316779'
FACEBOOK_APP_SECRET = '6fd8848bc9df865446ddcab34b098e26'


#: AWS
AWS_ACCESS_KEY_ID = 'AKIAIPUIPGMGOME2HTNQ'
AWS_SECRET_ACCESS_KEY = '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'
REGION = 'ap-northeast-1'


#: STEEM
STEEM_POSTING_KEY = ['5Jhz19vXUKHRVWsxBQpd58VdHvCSXAxNHW2rri645G7pWxy1onx']


# Application threads. A common general assumption is
# using 2 per available processor cores - to handle
# incoming requests using one and performing background
# operations using the other.
# THREADS_PER_PAGE = 2
