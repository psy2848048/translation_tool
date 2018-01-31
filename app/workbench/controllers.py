from flask import request, make_response, json, session, send_file, send_from_directory
import app.workbench.models as model
import io


def get_doc(did):
    doc_sentences = model.select_doc(did)
    return make_response(json.jsonify(results=doc_sentences), 200)


def get_trans_comments(did, sid):
    comments = model.select_trans_comments(sid)
    return make_response(json.jsonify(results=comments), 200)


def output_doc_to_file(did):
    output_type = request.values.get('type', None)

    if output_type is None:
        return make_response(json.jsonify('Something Not Entered'), 460)

    file, is_done = model.export_doc(output_type, did)

    if is_done is True:
        return send_file(io.BytesIO(file[0]), attachment_filename=file[1])
        # return send_file(io.BytesIO(file[0].encode('utf-8')), attachment_filename=file[1])
    else:
        return make_response(json.jsonify(result='Something Wrong! Is this document really complete?'), 461)


def save_trans_sentence(sid):
    trans_text = request.values.get('trans_text', None)
    trans_type = request.values.get('trans_type', None)

    is_done = model.insert_or_update_trans(sid, trans_text, trans_type)

    if is_done is True:
        return make_response(json.jsonify(result='OK'), 200)
    else:
        return make_response(json.jsonify(result='Something Wrong!'), 461)


def add_trans_comment(did, sid):
    # uid = session['uid']
    uid = 7
    comment = request.form.get('comment', None)

    if not comment:
        return make_response(json.jsonify('Something Not Entered'), 460)

    is_done = model.insert_trans_comment(uid, did, sid, comment)

    if is_done is True:
        return make_response(json.jsonify(result='OK'), 200)
    else:
        return make_response(json.jsonify(result='Something Wrong!'), 461)


def modify_sentence_status(sid, status):
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


def get_doc_comments(did):
    page = int(request.values.get('page', 1))
    rows = int(request.values.get('rows', 50))

    comments, total_cnt = model.select_doc_comments(did, page, rows)
    return make_response(json.jsonify(total_cnt=total_cnt, results=comments), 200)


def add_doc_comment(did):
    uid = 7
    comment = request.form.get('comment', None)

    if not comment:
        return make_response(json.jsonify('Something Not Entered'), 460)

    is_done = model.insert_doc_comment(uid, did, comment)

    if is_done is True:
        return make_response(json.jsonify(result='OK'), 200)
    else:
        return make_response(json.jsonify(result='Something Wrong!'), 461)


def delete_doc_comment(cid):
    uid = 7
    is_done = model.delete_trans_comment(cid)

    if is_done is True:
        return make_response(json.jsonify(result='OK'), 200)
    else:
        return make_response(json.jsonify(result='Something Wrong!'), 461)

