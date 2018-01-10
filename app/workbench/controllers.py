from flask import request, make_response, json, session
import app.workbench.models as model

def get_doc(did):
    doc_sentences = model.select_doc(did)
    return make_response(json.jsonify(results=doc_sentences), 200)

def save_new_trans_sentence(oid):
    text = request.values.get('text', None)
    trans_type = request.values.get('trans_type', None)

    is_done = model.insert_trans(oid, text, trans_type)

    if is_done == 1:
        return make_response(json.jsonify(result='OK'), 200)
    elif is_done == 2:
        return make_response(json.jsonify(result='Duplicate! 버전1에서는 하나의 원문당 하나의 번역문만 가질 수 있어요.'), 461)
    else:
        return make_response(json.jsonify(result='Something Wrong!'), 461)

def modify_trans_sentence(tid):
    text = request.values.get('text', None)
    trans_type = request.values.get('trans_type', None)

    is_done = model.update_trans(tid, text, trans_type)

    if is_done is True:
        return make_response(json.jsonify(result='OK'), 200)
    else:
        return make_response(json.jsonify(result='Something Wrong!'), 461)

def update_trans_status(tid, status):
    is_done = model.update_trans_status(tid, status)

    if is_done is True:
        return make_response(json.jsonify(result='OK'), 200)
    else:
        return make_response(json.jsonify(result='Something Wrong!'), 461)


##################################   comments   ##################################

def get_trans_comments(tid):
    comments = model.select_trans_comments(tid)
    return make_response(json.jsonify(results=comments), 200)

def make_trans_comment(tid):
    # uid = session['uid']
    uid = 5
    comment = request.form.get('comment', None)

    if not uid or not comment:
        return make_response(json.jsonify('Something Not Entered'), 460)

    is_done = model.insert_trans_comment(uid, tid, comment)

    if is_done is True:
        return make_response(json.jsonify(result='OK'), 200)
    else:
        return make_response(json.jsonify(result='Something Wrong!'), 461)

def delete_trans_comment(tid, cid):
    is_done = model.delete_trans_comment(cid)

    if is_done is True:
        return make_response(json.jsonify(result='OK'), 200)
    else:
        return make_response(json.jsonify(result='Something Wrong!'), 461)
