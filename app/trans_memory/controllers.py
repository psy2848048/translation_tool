from flask import request, make_response, json
import app.trans_memory.models as model


def get_trans_memory_list():
    page = int(request.values.get('page', 1))
    rows = int(request.values.get('rows', 30))

    tm, total_cnt = model.select_trans_memory(page, rows)
    return make_response(json.jsonify(total_cnt=total_cnt, results=tm), 200)


def save_trans_memory():
    #: 문장 하나만 받을 때
    # origin_lang = request.form.get('origin_lang', None)
    # trans_lang = request.form.get('trans_lang', None)
    # origin_text = request.form.get('origin_text', None)
    # trans_text = request.form.get('trans_text', None)

    #: CSV 파일로 받을 때
    file = request.files.get('file', None)

    # if not None in [origin_lang, trans_lang, origin_text, trans_text]:
    #     is_done = model.insert_trans_memory(origin_lang, trans_lang, origin_text, trans_text)
    # el
    if file is not None:
        if file.mimetype != 'text/csv':
            return make_response(json.jsonify(result='File mimetype is not CSV'), 461)

        is_done = model.insert_trans_memory_csv_file(file)
    else:
        return make_response(json.jsonify('Something Not Entered'), 460)

    if is_done is True:
        return make_response(json.jsonify(result='OK'), 200)
    else:
        return make_response(json.jsonify(result='Something Wrong!'), 461)


def modify_trans_memory(sid):
    origin_lang = request.form.get('origin_lang', None)
    trans_lang = request.form.get('trans_lang', None)
    origin_text = request.form.get('origin_text', None)
    trans_text = request.form.get('trans_text', None)

    is_done = model.update_trans_memory(sid, origin_lang, trans_lang, origin_text, trans_text)

    if is_done is True:
        return make_response(json.jsonify(result='OK'), 200)
    else:
        return make_response(json.jsonify(result='Something Wrong!'), 461)


def delete_trans_memory(sid):
    is_done = model.delete_trans_memory(sid)

    if is_done is True:
        return make_response(json.jsonify(result='OK'), 200)
    else:
        return make_response(json.jsonify(result='Something Wrong!'), 461)