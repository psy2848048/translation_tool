# -*- coding: utf-8 -*-
from flask import Flask, g, redirect, abort, make_response, jsonify
from flask_session import Session
from flask_cors import CORS
from flask_caching import Cache
from flasgger import Swagger
from flask_sqlalchemy import SQLAlchemy
from flask_sslify import SSLify

# Define the WSGI application object
app = Flask(__name__, static_url_path='/static', template_folder='/static/front')
app.static_folder = 'static'
app.template_folder = 'static/front'

#: Configurations
import config
app.config.from_object(config)

#: Swagger
#Swagger(app)

# Flask-Cache
cache = Cache(app, config={'CACHE_TYPE': 'simple'})

#: Flask-Session
Session(app)

#: Flask-CORS
cors = CORS(app, resources={r"/*": {"origins": "*", "supports_credentials": "true"}})

#: Flask_SSLify
sslify = SSLify(app)

###: DB 연결
# 저는 configs에 설정해서 바로 연결해서 쓸 수 있도록 했습니다.

# Import SQLAlchemy
# from flask.ext.sqlalchemy import SQLAlchemy
# from flask_sqlalchemy import SQLAlchemy

# Define the database object which is imported
# by modules and controllers
db = SQLAlchemy(app)

# Build the database:
# This will create the database file using SQLAlchemy
db.create_all()

#################################### 모듈 연결시키기 ####################################

# API Version
versions = ['/api/v1']

from app.auth.urls import auth
app.register_blueprint(auth, url_prefix='/api/v1/auth')

from app.users.urls import users
app.register_blueprint(users, url_prefix='/api/v1/users')

from app.projects.urls import projects
app.register_blueprint(projects, url_prefix='/api/v1/<int:uid>/projects')

from app.docs.urls import docs
app.register_blueprint(docs, url_prefix='/api/v1/<int:uid>/projects/docs')

from app.workbench.urls import workbench
app.register_blueprint(workbench, url_prefix='/api/v1/toolkit/workbench')

from app.trans_memory.urls import trans_memory
app.register_blueprint(trans_memory, url_prefix='/api/v1/toolkit/transMemory')

from app.termbase.urls import termbase
app.register_blueprint(termbase, url_prefix='/api/v1/toolkit/termbase')

from app.search.urls import search
app.register_blueprint(search, url_prefix='/api/v1/search')

#: 등록된 url 확인하기
print(app.url_map)

#####################################################################################


from app import common
from flask import request


@app.before_request
def before_request():
    """
    모든 API 실행 전 실행하는 부분
    """
    if '/api' in request.environ['PATH_INFO']:
        is_ok = common.ddos_check_and_write_log()
        if is_ok is False:
            return make_response(jsonify(result_en='Blocked connection'
                                         , result_ko='접속이 차단되었습니다'
                                         , result=503), 503)


@app.teardown_request
def teardown_request(exception):
    """
    모든 API 실행 후 실행하는 부분. 여기서는 DB 연결종료.
    """
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()


# Sample HTTP error handling
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify(result_ko='존재하지 않는 페이지입니다'
                                 , result_en='Not Found!'
                                 , result=404), 404)


@app.errorhandler(401)
def not_unauthorized(error):
    return make_response(jsonify(result_ko='인증되지 않음'
                                 , result_en='Unauthenticated'
                                 , result=401), 401)


@app.errorhandler(403)
def forbidden(error):
    # return abort(403)
    return make_response(jsonify(result_ko='접근 금지!'
                                 , result_en='Forbidden!'
                                 , result=403), 403)


@app.route('/')
def hello_world():
    return redirect('/static/index.html')
