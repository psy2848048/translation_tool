from flask import request, make_response, json
import app.comments.models as model

def index():
    return make_response(json.jsonify(msg='Search API'), 200)

def search(search_type):
    text = request.values.get('text', None)
