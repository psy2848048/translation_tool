from flask import request, make_response, json
import app.docs.models as model

def get_doc_info(uid, did):
    doc_info = model.select_doc_info(did)
    return make_response(json.jsonify(doc_info), 200)

def get_doc_members(uid, did):
    page = int(request.values.get('page', 1))
    rows = int(request.values.get('rows', 10))

    doc_members, total_cnt = model.select_doc_members(did, page, rows)
    return make_response(json.jsonify(total_cnt=total_cnt, results=doc_members), 200)


def modify_doc_info(uid, did):
    title = request.form.get('title', None)
    status = request.form.get('status', None)
    link = request.form.get('link', None)
    origin_lang = request.form.get('origin_lang', None)
    trans_lang = request.form.get('trans_lang', None)
    due_date = request.form.get('due_date', None)

    if None in [title, status, origin_lang, trans_lang, due_date]:
        return make_response(json.jsonify(result='Something Not Entered'), 460)

    is_done = model.update_doc_info(did, title, status, link, origin_lang, trans_lang, due_date)

    #: 문서 상태가 완료된 경우 원문과 번역문을 문장저장소에 저장한다
    if status == '완료' or status == 3:
        pass

    if is_done is True:
        return make_response(json.jsonify(result='OK'), 200)
    else:
        return make_response(json.jsonify(result='Something Wrong!'), 461)

def modify_doc_member(uid, did, mid):
    can_read = request.form.get('can_read', None)
    can_modify = request.form.get('can_modify', None)
    can_delete = request.form.get('can_delete', None)

    if None in [can_read, can_modify, can_delete]:
        return make_response(json.jsonify(result='Something Not Entered'), 460)

    is_done = model.update_doc_member(did, mid, can_read, can_modify, can_delete)

    if is_done is True:
        return make_response(json.jsonify(result='OK'), 200)
    else:
        return make_response(json.jsonify(result='Something Wrong!'), 461)


def delete_doc(uid, did):
    is_done = model.delete_doc(did)

    if is_done is True:
        return make_response(json.jsonify(result='OK'), 200)
    else:
        return make_response(json.jsonify(result='Something Wrong!'), 461)

