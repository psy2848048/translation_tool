from flask import request, make_response, json
from flask_login import login_required, current_user
import app.termbase.models as model


@login_required
def get_termbase_list():
    uid = current_user.idx
    origin_lang = request.values.get('origin_lang', None)
    trans_lang = request.values.get('trans_lang', None)
    page = int(request.values.get('page', 1))
    rows = int(request.values.get('rows', 30))

    if None in [origin_lang, trans_lang]:
        return make_response(json.jsonify('Something Not Entered'), 460)

    terms, total_cnt = model.select_termbase(uid, origin_lang, trans_lang, page, rows)
    return make_response(json.jsonify(total_cnt=total_cnt, results=terms), 200)


@login_required
def save_termbase():
    uid = current_user.idx
    origin_lang = request.form.get('origin_lang', None)
    trans_lang = request.form.get('trans_lang', None)
    origin_text = request.form.get('origin_text', None)
    trans_text = request.form.get('trans_text', None)
    file = request.files.get('file', None)

    tbid = 0
    if not None in [origin_lang, trans_lang, origin_text, trans_text]:
        is_done, tbid = model.insert_term(uid, origin_lang, trans_lang, origin_text, trans_text)
    elif file is not None:
        if file.mimetype != 'text/csv':
            return make_response(json.jsonify(result='File mimetype is not CSV'), 461)

        is_done = model.insert_term_csv_file(uid, file, origin_lang, trans_lang)
    else:
        return make_response(json.jsonify('Something Not Entered'), 460)

    if is_done is True:
        return make_response(json.jsonify(tbid=tbid), 200)
    else:
        return make_response(json.jsonify(result='Something Wrong!'), 461)


@login_required
def modify_term(tbid):
    origin_lang = request.form.get('origin_lang', None)
    trans_lang = request.form.get('trans_lang', None)
    origin_text = request.form.get('origin_text', None)
    trans_text = request.form.get('trans_text', None)

    msg, updated_tb = model.update_term(tbid, origin_lang, trans_lang, origin_text, trans_text)

    if msg is 'OK':
        return make_response(json.jsonify(updated_tb), 200)
    else:
        return make_response(json.jsonify(result=msg), 461)


@login_required
def delete_term(tbid):
    is_done, deleted_tbid = model.delete_term(tbid)

    if is_done is True:
        return make_response(json.jsonify(tbid=deleted_tbid), 200)
    else:
        return make_response(json.jsonify(result='Something Wrong!'), 461)
