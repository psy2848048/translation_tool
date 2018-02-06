# -*- coding: utf-8 -*-
from app import app
from gevent.wsgi import WSGIServer

#: HTTPS, SSL 설정
cert = './cert_key/mysite.cert.pem'
key = './cert_key/mysite.key.pem'

# http = WSGIServer(('0.0.0.0', 5000), app)
# http.serve_forever()
https = WSGIServer(('0.0.0.0', 5001), app, keyfile=key, certfile=cert)
https.serve_forever()
