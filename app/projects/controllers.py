from flask import request, make_response, json
from flask_login import login_required, current_user
import app.projects.models as model
from app import common


@login_required
def get_projects_list():
    uid = current_user.idx
    page = int(request.values.get('page', 1))
    rows = int(request.values.get('rows', 15))

    projects, total_cnt = model.select_projects(uid, page, rows)
    return make_response(json.jsonify(total_cnt=total_cnt, results=projects), 200)


@login_required
def get_project_info(pid):
    project_info = model.select_project_info(pid)
    return make_response(json.jsonify(project_info), 200)


@login_required
def get_proejct_docs(pid):
    page = int(request.values.get('page', 1))
    rows = int(request.values.get('rows', 15))

    project_docs, total_cnt = model.select_project_docs(pid, page, rows)
    return make_response(json.jsonify(total_cnt=total_cnt, results=project_docs), 200)


@login_required
def get_proejct_members(pid):
    page = int(request.values.get('page', 1))
    rows = int(request.values.get('rows', 10))

    project_members, total_cnt = model.select_project_members(pid, page, rows)
    return make_response(json.jsonify(total_cnt=total_cnt, results=project_members), 200)


@login_required
def add_project():
    uid = current_user.idx
    name = request.form.get('name', None)
    due_date = request.form.get('due_date', None)

    if name is None:
        return make_response(json.jsonify(result='Something Not Entered'), 460)

    if len(due_date) < 3:
        due_date = None
    elif due_date is not None:
        due_date = common.convert_datetime4mysql(due_date)

    is_done = model.insert_project(uid, name, due_date)

    if is_done is True:
        return make_response(json.jsonify(result='OK'), 200)
    else:
        return make_response(json.jsonify(result='Something Wrong!'), 461)


@login_required
def add_doc(pid):
    title = request.form.get('title', None)
    origin_lang = request.form.get('origin_lang', None)
    trans_lang = request.form.get('trans_lang', None)
    due_date = request.form.get('due_date', None)
    type = request.form.get('type', None)
    content = request.form.get('content', None)

    #: 사용자 권한 검사
    uid = current_user.idx
    user_auth = model.select_project_access_auth(uid, pid)
    if user_auth['can_create_doc'] != 1:
        return make_response(json.jsonify(result='You do not have authority to create documents'), 403)

    #: Request Data 검사
    if None in [title, origin_lang, trans_lang, type]:
        return make_response(json.jsonify(result='Something Not Entered'), 460)
    elif not content and type == 'text':
        return make_response(json.jsonify(result='Something Not Entered'), 460)

    if len(due_date) < 3:
        due_date = None
    elif due_date is not None:
        due_date = common.convert_datetime4mysql(due_date)

    is_done = model.insert_doc(pid, title, origin_lang, trans_lang, due_date, type, content)

    if is_done is True:
        return make_response(json.jsonify(result='OK'), 200)
    else:
        return make_response(json.jsonify(result='Something Wrong!'), 461)


@login_required
def add_project_member(pid):
    mid = request.form.get('mid', None)
    can_read = request.form.get('can_read', None)
    can_modify = request.form.get('can_modify', None)
    can_delete = request.form.get('can_delete', None)
    can_create_doc = request.form.get('can_create_doc', None)

    #: 사용자 권한 검사
    # uid = current_user.idx
    # user_auth = model.select_project_access_auth(uid, pid)
    # if user_auth['can_read'] != 1:
    #     return make_response(json.jsonify(result='You do not have authority'), 403)

    #: Request Data 검사
    if None in [mid, can_read, can_modify, can_delete, can_create_doc]:
        return make_response(json.jsonify(result='Something Not Entered'), 460)

    is_done = model.insert_project_member(pid, mid, can_read, can_modify, can_delete, can_create_doc)

    if is_done is 1:
        return make_response(json.jsonify(result='OK'), 200)
    elif is_done is 2:
        return make_response(json.jsonify(result='DUP'), 260)
    else:
        return make_response(json.jsonify(result='Something Wrong!'), 461)


@login_required
def modify_project_info(pid):
    name = request.form.get('name', None)
    status = request.form.get('status', None)
    due_date = request.form.get('due_date', None)

    #: 사용자 권한 검사
    uid = current_user.idx
    user_auth = model.select_project_access_auth(uid, pid)
    if user_auth['can_modify'] != 1:
        return make_response(json.jsonify(result='You do not have authority to modify project'), 403)

    #: Request Data 검사
    if None in [name, status]:
        return make_response(json.jsonify(result='Something Not Entered'), 460)
    if status not in ['신규', '진행중', '완료', '취소']:
        return make_response(json.jsonify(result='Status is wrong'), 461)

    if len(due_date) < 3:
        due_date = None
    elif due_date is not None:
        due_date = common.convert_datetime4mysql(due_date)

    is_done = model.update_project_info(pid, name, status, due_date)

    if is_done is True:
        return make_response(json.jsonify(result='OK'), 200)
    else:
        return make_response(json.jsonify(result='Something Wrong!'), 461)


@login_required
def modify_project_member(pid, mid):
    can_read = request.form.get('can_read', None)
    can_modify = request.form.get('can_modify', None)
    can_delete = request.form.get('can_delete', None)
    can_create_doc = request.form.get('can_create_doc', None)

    #: 사용자 권한 검사
    # uid = current_user.idx
    # user_auth = model.select_project_access_auth(uid, pid)
    # if user_auth['can_create_doc'] != 1:
    #     return make_response(json.jsonify(result='You do not have authority to create documents'), 403)

    #: Request Data 검사
    if None in [can_read, can_modify, can_delete, can_create_doc]:
        return make_response(json.jsonify(result='Something Not Entered'), 460)

    is_done = model.update_project_member(pid, mid, can_read, can_modify, can_delete, can_create_doc)

    if is_done is True:
        return make_response(json.jsonify(result='OK'), 200)
    else:
        return make_response(json.jsonify(result='Something Wrong!'), 461)


@login_required
def delete_project(pid):
    #: 사용자 권한 검사
    uid = current_user.idx
    user_auth = model.select_project_access_auth(uid, pid)
    if user_auth['can_delete'] != 1:
        return make_response(json.jsonify(result='You do not have authority to delete project'), 403)

    is_done = model.delete_project(pid)

    if is_done is True:
        return make_response(json.jsonify(result='OK'), 200)
    else:
        return make_response(json.jsonify(result='Something Wrong!'), 461)


@login_required
def delete_project_member(pid, mid):
    #: 프로젝트 개설자는 삭제될 수 없다
    user_auth = model.select_project_access_auth(mid, pid)
    if user_auth['is_founder'] == 1:
        return make_response(json.jsonify(result=463), 200)

    is_done = model.delete_project_member(mid, pid)

    if is_done is True:
        return make_response(json.jsonify(result='OK'), 200)
    else:
        return make_response(json.jsonify(result='Something Wrong!'), 461)
