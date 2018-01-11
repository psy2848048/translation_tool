from flask import request, make_response, json
import app.users.models as model

def sign_up():
    name = request.form.get('name', None)
    email = request.form.get('email', None)
    password = request.form.get('password', None)

    is_done = model.insert_user(name, email, password)

    if is_done is True:
        return make_response(json.jsonify(result='OK'), 200)
    else:
        return make_response(json.jsonify(result='Something Wrong!'), 461)
