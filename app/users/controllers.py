from flask import request, make_response, json
import app.users.models as model

def index(user_id):
    # return 'Project API'
    return make_response(json.jsonify(msg='Project API', user_id=user_id), 200)

def signup():
    email = request.form.get('email', None)
    username = request.form.get('username', None)
    password = request.form.get('password', None)

    if not email or not username or not password:
        return make_response(json.jsonify('Something not Entered'), 400)

def get_user_info(user_id):
    return make_response(json.jsonify(result=''), 200)

def modify_user_info(user_id):
    return make_response(json.jsonify(result=''), 200)
