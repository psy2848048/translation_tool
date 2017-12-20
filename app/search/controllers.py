from flask import request, make_response, json
import app.search.models as model

def index():
    return make_response(json.jsonify(msg='Search API'), 200)

def search(search_type):
    return make_response(json.jsonify(result=''), 200)

def search_word():
    text = request.values.get('text', None)

    results = []
    words = model.select_word(text.lower())
    for w in words:
        results.append(dict(w))

    return make_response(json.jsonify(result=results), 200)