from flask import request, make_response, json
from flask_login import login_required, current_user
import app.docs.models as model
from app import common


@login_required
def get_doc_info(did):
    doc_info = model.select_doc_info(did)
    return make_response(json.jsonify(doc_info), 200)


@login_required
def get_doc_members(did):
    page = int(request.values.get('page', 1))
    rows = int(request.values.get('rows', 10))

    doc_members, total_cnt = model.select_doc_members(did, page, rows)
    return make_response(json.jsonify(total_cnt=total_cnt, results=doc_members), 200)


@login_required
def modify_doc_info(did):
    title = request.form.get('title', None)
    status = request.form.get('status', None)
    link = request.form.get('link', None)
    origin_lang = request.form.get('origin_lang', None)
    trans_lang = request.form.get('trans_lang', None)
    due_date = request.form.get('due_date', None)

    if None in [title, status, origin_lang, trans_lang]:
        return make_response(json.jsonify(result='Something Not Entered'), 460)
    if status not in ['신규', '진행중', '완료', '취소']:
        return make_response(json.jsonify(result='Status is wrong'), 461)

    if len(due_date) < 3:
        due_date = None
    elif due_date is not None:
        due_date = common.convert_datetime_4mysql(due_date)

    is_done = model.update_doc_info(did, title, status, link, origin_lang, trans_lang, due_date)

    #: 문서 상태가 완료된 경우 원문과 번역문을 문장저장소에 저장한다
    if status == '완료' or status == 3:
        pass

    if is_done is True:
        return make_response(json.jsonify(result='OK'), 200)
    else:
        return make_response(json.jsonify(result='Something Wrong!'), 461)


@login_required
def modify_doc_member(did, mid):
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


@login_required
def delete_doc(did):
    is_done = model.delete_doc(did)

    if is_done is True:
        return make_response(json.jsonify(result='OK'), 200)
    else:
        return make_response(json.jsonify(result='Something Wrong!'), 461)

