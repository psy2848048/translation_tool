from flask import request, make_response, json
import app.projects.models as model

def index(user_id):
    return make_response(json.jsonify(msg='Projects API', user_id=user_id), 200)

def get_projects_list(user_id):
    projects = []
    results = model.select_projects(user_id)
    for project in results:
        print(project)
        projects.append(dict(project))

    return make_response(json.jsonify(result=projects), 200)

def make_project(user_id):
    project_name = request.form.get('project_name', None)
    client_company = request.form.get('client_company', None)
    clients = request.form.get('clients', None)
    origin_lang = request.form.get('origin_lang', None)
    trans_lang = request.form.get('trans_lang', None)

    if not user_id or not project_name or not client_company or not clients or not origin_lang or not trans_lang:
        return make_response(json.jsonify('Something Not Entered'), 460)

    return make_response(json.jsonify(result=''), 200)

def modify_project(user_id):
    return make_response(json.jsonify(result=''), 200)

def delete_project(user_id):
    return make_response(json.jsonify(result=''), 200)


def get_project_info(user_id, project_id):
    return make_response(json.jsonify(result=''), 200)


def get_project_members(user_id, project_id):
    return make_response(json.jsonify(result=''), 200)

def add_project_member(user_id, project_id):
    return make_response(json.jsonify(result=''), 200)

def delete_project_members(user_id, project_id):
    return make_response(json.jsonify(result=''), 200)
