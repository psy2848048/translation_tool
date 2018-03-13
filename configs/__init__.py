# -*- coding: utf-8 -*-
from datetime import timedelta
import os


class Config(object):
    VERSION = '0.1'
    DEBUG = True

    # Define the application directory
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))

    PORT = 5001
    HOST=''
    #SESSION_COOKIE_DOMAIN=".ciceron.me"
    #SESSION_COOKIE_PATH="/"

    SSL_KEY = './configs/cert_key/pfx.mycattool_com.key'
    SSL_CERT = './configs/cert_key/pfx.mycattool_com.crt'

    #: Session
    SESSION_TYPE = 'redis'
    SESSION_COOKIE_NAME = "MyCatToolCookie"
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=30)
    SECRET_KEY = os.urandom(24)

    #: Swagger
    SWAGGER = {
        'title': 'MyCatTool API',
        'uiversion': 2
    }

    #: SQLAlchemy, DB
    DATABASE_CONFIG = {
        'driver': 'mysql+pymysql',
        'host': 'ciceronservice2.cng6yzqtxqhh.ap-northeast-1.rds.amazonaws.com',
        'dbname': 'marocat v1.1',
        'user': 'root',
        'password': 'ciceron01!',
        'port': 3306
    }
    SQLALCHEMY_DATABASE_URI = '{driver}://{user}:{password}@{host}/{dbname}'.format(**DATABASE_CONFIG)
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    #: JSON으로 들어온 데이터들을 정렬해준다
    JSON_SORT_KEYS=False
    MAX_CONTENT_LENGTH=5 * 1024 * 1024
    UPLOAD_FOLDER_RESULT="results"

    #: Google
    GOOGLE_CLIENT_SECRETS_FILE = './configs/google_client_secret.json'

    #: Facebook
    FACEBOOK_APP_ID = '931700420316779'
    FACEBOOK_APP_SECRET = '6fd8848bc9df865446ddcab34b098e26'

    #: AWS
    AWS_ACCESS_KEY_ID = 'AKIAIPUIPGMGOME2HTNQ'
    AWS_SECRET_ACCESS_KEY = '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'
    REGION = 'ap-northeast-1'

    #: STEEM
    STEEM_POSTING_KEY = ['5Jhz19vXUKHRVWsxBQpd58VdHvCSXAxNHW2rri645G7pWxy1onx']

    # Application threads. A common general assumption is using 2 per available processor cores
    # - to handle incoming requests using one and performing background operations using the other.
    # THREADS_PER_PAGE = 2


class ProdConfig(Config):
    PORT = 443
    HOST = ''
    #SESSION_COOKIE_DOMAIN=".ciceron.me"
    #SESSION_COOKIE_PATH="/"


class DevConfig(Config):
    PORT = 5001
    HOST = ''
    #SESSION_COOKIE_DOMAIN=".ciceron.me"
    #SESSION_COOKIE_PATH="/"


class TestConfig(Config):
    HOST = ''
    #SESSION_COOKIE_DOMAIN=".ciceron.me"
    #SESSION_COOKIE_PATH="/"

