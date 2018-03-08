# -*- coding: utf-8 -*-
from app import app
from gevent.wsgi import WSGIServer
import os

#: HTTPS, SSL 설정
cert = './cert_key/pfx.mycattool_com.crt'
key = './cert_key/pfx.mycattool_com.key'

https = None
if os.environ.get('PURPOSE') == 'PROD':
    https = WSGIServer(('0.0.0.0', 443), app, keyfile=key, certfile=cert)
else:
    https = WSGIServer(('0.0.0.0', 5001), app, keyfile=key, certfile=cert)
https.serve_forever()

# http = WSGIServer(('0.0.0.0', 5000), app)
