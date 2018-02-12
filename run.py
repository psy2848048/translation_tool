# -*- coding: utf-8 -*-
from app import app
from gevent.wsgi import WSGIServer

#: HTTPS, SSL 설정
cert = './cert_key/pfx.mycattool_com.crt'
key = './cert_key/pfx.mycattool_com.key'

# http = WSGIServer(('0.0.0.0', 5000), app)
https = WSGIServer(('0.0.0.0', 5001), app, keyfile=key, certfile=cert)
https = WSGIServer(('0.0.0.0', 443), app, keyfile=key, certfile=cert)
# https.serve_forever()
