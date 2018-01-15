from flask import request, make_response, json, session
import app.workbench.models as model


def get_doc(did):
    doc_sentences = model.select_doc(did)
    return make_response(json.jsonify(results=doc_sentences), 200)


def get_trans_comments(sid):
    comments = model.select_trans_comments(sid)
    return make_response(json.jsonify(results=comments), 200)


def output_doc_to_file(did):
    file, http_code = model.export_doc_as_csv(did)


def save_trans_sentence(sid):
    trans_text = request.values.get('trans_text', None)
    trans_type = request.values.get('trans_type', None)

    is_done = model.insert_or_update_trans(sid, trans_text, trans_type)

    if is_done is True:
        return make_response(json.jsonify(result='OK'), 200)
    else:
        return make_response(json.jsonify(result='Something Wrong!'), 461)


def make_trans_comment(sid):
    # uid = session['uid']
    uid = request.values.get('uid', None)   # 사용자 붙이면 없어질 예정
    comment = request.form.get('comment', None)

    if not uid or not comment:
        return make_response(json.jsonify('Something Not Entered'), 460)

    is_done = model.insert_trans_comment(uid, sid, comment)

    if is_done is True:
        return make_response(json.jsonify(result='OK'), 200)
    else:
        return make_response(json.jsonify(result='Something Wrong!'), 461)


def save_sentence_status(sid, status):
    is_done = model.update_sentence_status(sid, status)

    if is_done is True:
        return make_response(json.jsonify(result='OK'), 200)
    else:
        return make_response(json.jsonify(result='Something Wrong!'), 461)


def delete_trans_comment(cid):
    is_done = model.delete_trans_comment(cid)

    if is_done is True:
        return make_response(json.jsonify(result='OK'), 200)
    else:
        return make_response(json.jsonify(result='Something Wrong!'), 461)
