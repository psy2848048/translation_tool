from flask import request, make_response, json
import app.termbase.models as model
from io import TextIOWrapper

def get_termbase_list():
    page = int(request.values.get('page', 1))
    rows = int(request.values.get('rows', 30))

    terms, total_cnt = model.select_termbase(page, rows)
    return make_response(json.jsonify(total_cnt=total_cnt, results=terms), 200)

def save_termbase():
    #: 단어 하나만 받을 때
    origin_lang = request.form.get('origin_lang', None)
    trans_lang = request.form.get('trans_lang', None)
    origin_text = request.form.get('origin_text', None)
    trans_text = request.form.get('trans_text', None)

    #: CSV 파일로 받을 때
    file = TextIOWrapper(request.files.get('file', None))

    if not None in [origin_lang, trans_lang, origin_text, trans_text]:
        is_done = model.insert_term(origin_lang, trans_lang, origin_text, trans_text)
    elif file is not None:
        is_done = model.insert_term_csv_file(file, origin_lang, trans_lang)
    else:
        return make_response(json.jsonify('Something Not Entered'), 460)

    if is_done is True:
        return make_response(json.jsonify(result='OK'), 200)
    else:
        return make_response(json.jsonify(result='Something Wrong!'), 461)

def modify_term(tid):
    origin_lang = request.form.get('origin_lang', None)
    trans_lang = request.form.get('trans_lang', None)
    origin_text = request.form.get('origin_text', None)
    trans_text = request.form.get('trans_text', None)

    is_done = model.update_term(tid, origin_lang, trans_lang, origin_text, trans_text)

    if is_done is True:
        return make_response(json.jsonify(result='OK'), 200)
    else:
        return make_response(json.jsonify(result='Something Wrong!'), 461)

def modify_term_trans(tid):
    trans_text = request.form.get('trans_text', None)

    is_done = model.update_term_trans(tid, trans_text)

    if is_done is True:
        return make_response(json.jsonify(result='OK'), 200)
    else:
        return make_response(json.jsonify(result='Something Wrong!'), 461)
