from flask import request, make_response, json
import app.projects.models as model
import nltk

def index(uid):
    return make_response(json.jsonify(msg='Projects API', uid=uid), 200)

def get_projects_list(uid):
    page = int(request.values.get('page', 1))
    rows = int(request.values.get('rows', 15))

    projects, total_cnt = model.select_projects(uid, page, rows)
    return make_response(json.jsonify(total_cnt=total_cnt, results=projects), 200)

def get_project_info(uid, pid):
    project_info = model.select_project_info(pid)
    return make_response(json.jsonify(project_info), 200)

def get_proejct_docs(uid, pid):
    page = int(request.values.get('page', 1))
    rows = int(request.values.get('rows', 15))

    project_docs, total_cnt = model.select_project_docs(pid, page, rows)
    return make_response(json.jsonify(total_cnt=total_cnt, results=project_docs), 200)

def get_proejct_members(uid, pid):
    page = int(request.values.get('page', 1))
    rows = int(request.values.get('rows', 10))

    project_members, total_cnt = model.select_project_members(pid, page, rows)
    return make_response(json.jsonify(total_cnt=total_cnt, results=project_members), 200)


def make_project(uid):
    name = request.form.get('name', None)
    due_date = request.form.get('due_date', None)

    if None in [name, due_date]:
        return make_response(json.jsonify(result='Something Not Entered'), 460)

    is_done = model.insert_project(uid, name, due_date)

    if is_done is True:
        return make_response(json.jsonify(result='OK'), 200)
    else:
        return make_response(json.jsonify(result='Something Wrong!'), 461)

def add_doc(uid, pid):
    title = request.form.get('title', None)
    origin_lang = request.form.get('origin_lang', None)
    trans_lang = request.form.get('trans_lang', None)
    due_date = request.form.get('due_date', None)
    type = request.form.get('type', None)
    content = request.form.get('content', None)
    file = request.files.get('file', None)

    if None in [title, origin_lang, trans_lang, due_date, type]:
        return make_response(json.jsonify(result='Something Not Entered'), 460)
    elif not content and type == 'text':
        return make_response(json.jsonify(result='Something Not Entered'), 460)

    if type == 'text':
        # 내용을 문장 단위로 나누기 - 내용을 통으로 넣으면 배열로 문장이 하나씩 갈라져 나온다
        sentences = nltk.data.load('tokenizers/punkt/english.pickle').tokenize(content)
        is_done = model.insert_doc_and_sentences(pid, title, origin_lang, trans_lang, due_date, type, sentences)
    else:
        is_done = False

    if is_done is True:
        return make_response(json.jsonify(result='OK'), 200)
    else:
        return make_response(json.jsonify(result='Something Wrong!'), 461)

def add_project_member(uid, pid):
    uid = request.form.get('user_id', None)
    can_read = request.form.get('can_read', None)
    can_modify = request.form.get('can_modify', None)
    can_delete = request.form.get('can_delete', None)
    can_create_doc = request.form.get('can_create_doc', None)

    if None in [uid, can_read, can_modify, can_delete, can_create_doc]:
        return make_response(json.jsonify(result='Something Not Entered'), 460)

    is_done = model.insert_project_member(pid, uid, can_read, can_modify, can_delete, can_create_doc)

    if is_done is True:
        return make_response(json.jsonify(result='OK'), 200)
    else:
        return make_response(json.jsonify(result='Something Wrong!'), 461)


def modify_project_info(uid, pid):
    name = request.form.get('name', None)
    status = request.form.get('status', None)
    due_date = request.form.get('due_date', None)

    if None in [name, status, due_date]:
        return make_response(json.jsonify(result='Something Not Entered'), 460)

    is_done = model.update_project_info(pid, name, status, due_date)

    if is_done is True:
        return make_response(json.jsonify(result='OK'), 200)
    else:
        return make_response(json.jsonify(result='Something Wrong!'), 461)

def modify_project_member(uid, pid, mid):
    can_read = request.form.get('can_read', None)
    can_modify = request.form.get('can_modify', None)
    can_delete = request.form.get('can_delete', None)
    can_create_doc = request.form.get('can_create_doc', None)

    if None in [can_read, can_modify, can_delete, can_create_doc]:
        return make_response(json.jsonify(result='Something Not Entered'), 460)

    is_done = model.update_project_member(pid, mid, can_read, can_modify, can_delete, can_create_doc)

    if is_done is True:
        return make_response(json.jsonify(result='OK'), 200)
    else:
        return make_response(json.jsonify(result='Something Wrong!'), 461)


def delete_project(uid, pid):
    is_done = model.delete_project(pid)

    if is_done is True:
        return make_response(json.jsonify(result='OK'), 200)
    else:
        return make_response(json.jsonify(result='Something Wrong!'), 461)

def delete_project_member(uid, pid, mid):
    is_done = model.delete_project_member(pid, mid)

    if is_done is True:
        return make_response(json.jsonify(result='OK'), 200)
    else:
        return make_response(json.jsonify(result='Something Wrong!'), 461)