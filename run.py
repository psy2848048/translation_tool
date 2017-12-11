# -*- coding: utf-8 -*-
from app import app
from gevent.wsgi import WSGIServer

#: HTTPS, SSL 설정
# cert = './cert_key/mysite.cert.pem'
# key = './cert_key/mysite.key.pem'

#: Method 1. 스레드 하나만 돌릴 때
http = WSGIServer(('0.0.0.0', 80), app)
http.serve_forever()
