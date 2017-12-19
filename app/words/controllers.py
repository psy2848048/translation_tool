from flask import request, make_response, json
import app.words.models as model

def index(user_id):
    return make_response(json.jsonify(msg='Words API', user_id=user_id), 200)

def get_words(user_id):
    results = []

    words = model.select_word_memory()
    for w in words:
        results.append(dict(w))

    return make_response(json.jsonify(result=results), 200)

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

    is_done = model.insert_word_memory(origin_lang, trans_lang, origin_text, trans_text)

    if is_done is True:
        return make_response(json.jsonify(result='OK'), 200)
    else:
        return make_response(json.jsonify(result='Something Wrong!'), 461)

def modify_word(user_id, word_id):
    origin_lang = request.form.get('origin_lang', None)
    trans_lang = request.form.get('trans_lang', None)
    origin_text = request.form.get('origin_text', None)
    trans_text = request.form.get('trans_text', None)

    is_done = model.update_word(word_id, origin_lang, trans_lang, origin_text, trans_text)

    if is_done is True:
        return make_response(json.jsonify(result='OK'), 200)
    else:
        return make_response(json.jsonify(result='Something Wrong!'), 461)
