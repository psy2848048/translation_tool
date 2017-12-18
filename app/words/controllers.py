from flask import request, make_response, json
import app.words.models as model

def index(user_id):
    return make_response(json.jsonify(msg='Words API', user_id=user_id), 200)

def get_words(user_id):
    return make_response(json.jsonify(result=''), 200)

def save_words_files(user_id):
    files = request.files.get('files', None)
    if not files:
        return make_response(json.jsonify('Something Not Entered'), 460)

    return make_response(json.jsonify(result=''), 200)

def save_word(user_id):
    origin_lang = request.form.get('origin_lang', None)
    trans_lang = request.form.get('trans_lang', None)
    origin_text = request.form.get('origin_text', None)
    trans_text = request.form.get('trans_text', None)

    if not origin_lang or not trans_lang or not origin_text or not trans_text:
        return make_response(json.jsonify('Something Not Entered'), 460)

    return make_response(json.jsonify(result=''), 200)

def modify_word(user_id, word_id):
    trans_text = request.form.get('trans_text', None)

    if not trans_text:
        return make_response(json.jsonify('Something Not Entered'), 460)

    return make_response(json.jsonify(result=''), 200)