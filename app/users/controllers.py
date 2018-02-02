from flask import request, make_response, json
from flask_login import login_required, current_user
import app.users.models as model


@login_required
def get_user_info():
    return make_response(json.jsonify(current_user.info), 200)


@login_required
def change_password():
    old_pwd = request.form.get('old_pwd', None)
    new_pwd = request.form.get('new_pwd', None)

    is_done, http_code = model.update_password(current_user.id, old_pwd, new_pwd)

    if is_done is True:
        return make_response(json.jsonify(result='OK'), http_code)
    elif http_code == 401:
        return make_response(json.jsonify(result='Password is wrong'), http_code)
    elif http_code == 461:
        return make_response(json.jsonify(result='Something Wrong!'), http_code)
    elif http_code == 462:
        return make_response(json.jsonify(result='Duplicate!'), http_code)