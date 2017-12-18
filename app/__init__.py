# -*- coding: utf-8 -*-
from flask import Flask, g, redirect, abort
from flask_session import Session
from flask_cors import CORS
from flask_caching import Cache
from flasgger import Swagger
from flask_sqlalchemy import SQLAlchemy

# Define the WSGI application object
app = Flask(__name__, static_url_path='/static')
app.static_folder = 'static'

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
app.register_blueprint(projects, url_prefix='/api/v1/users/<int:user_id>/projects')

from app.docs.urls import docs
app.register_blueprint(docs, url_prefix='/api/v1/users/<int:user_id>/docs')

from app.translation.urls import translation
app.register_blueprint(translation, url_prefix='/api/v1/users/<int:user_id>/translation')

from app.comments.urls import comments
app.register_blueprint(comments, url_prefix='/api/v1/users/<int:user_id>/comments')

from app.words.urls import words
app.register_blueprint(words, url_prefix='/api/v1/users/<int:user_id>/words')

from app.search.urls import search
app.register_blueprint(search, url_prefix='/api/v1/search')

#: 등록된 url 확인하기
print(app.url_map)

#####################################################################################

@app.before_request
def before_request():
    """
    모든 API 실행 전 실행하는 부분
    """
    pass

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
    return 'Not Found!!!!!'

@app.errorhandler(403)
def not_loggedIn(error):
    return abort(403)

@app.route('/')
def hello_world():
    return redirect('/static/index.html')
