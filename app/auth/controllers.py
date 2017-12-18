from flask import request, make_response, json
import app.auth.models as model

def index():
    return make_response(json.jsonify(msg='Auth API'), 200)
