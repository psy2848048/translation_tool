from flask import request, make_response, json
import app.translation.models as model

def index(user_id):
    return make_response(json.jsonify(msg='Projects API', user_id=user_id), 200)

def get_translate_and_words(user_id, sentence_id):
    origin_text = request.form.get('origin_text', None)

    if not origin_text:
        return make_response(json.jsonify('Something Not Entered'), 460)

    return make_response(json.jsonify(result=''), 200)

def save_translation(user_id, sentence_id):
    trans_type = request.form.get('trans_type', None)
    trans_text = request.form.get('trans_text', None)

    if not trans_type or not trans_text:
        return make_response(json.jsonify('Something Not Entered'), 460)

    return make_response(json.jsonify(result=''), 200)

def save_translation_status(user_id, sentence_id, status):
    return make_response(json.jsonify(result=''), 200)
