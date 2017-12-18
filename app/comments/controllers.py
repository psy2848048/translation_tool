from flask import request, make_response, json
import app.comments.models as model

def index(user_id):
    return make_response(json.jsonify(msg='Projects API', user_id=user_id), 200)

def get_comments(user_id):
    project_id = request.args.get('project_id', None)
    doc_id = request.args.get('doc_id', None)
    sentence_id = request.args.get('sentence_id', None)

    if not project_id or not doc_id or not sentence_id:
        return make_response(json.jsonify('Something Not Entered'), 460)

    return make_response(json.jsonify(result=''), 200)

def make_comment(user_id):
    project_id = request.values.get('project_id', None)
    doc_id = request.values.get('doc_id', None)
    sentence_id = request.values.get('sentence_id', None)
    comment = request.form.get('comments', None)

    if not project_id or not doc_id or not sentence_id or not comment:
        return make_response(json.jsonify('Something Not Entered'), 460)

    return make_response(json.jsonify(result=''), 200)

def modify_comment(user_id, comment_id):
    project_id = request.values.get('project_id', None)
    doc_id = request.values.get('doc_id', None)
    sentence_id = request.values.get('sentence_id', None)
    comments = request.form.get('comments', None)

    if not project_id or not doc_id or not sentence_id:
        return make_response(json.jsonify('Something Not Entered'), 460)

    return make_response(json.jsonify(result=''), 200)

def delete_comment(user_id, comment_id):
    project_id = request.values.get('project_id', None)
    doc_id = request.values.get('doc_id', None)
    sentence_id = request.values.get('sentence_id', None)
    comments = request.form.get('comments', None)

    if not project_id or not doc_id or not sentence_id:
        return make_response(json.jsonify('Something Not Entered'), 460)

    return make_response(json.jsonify(result=''), 200)

