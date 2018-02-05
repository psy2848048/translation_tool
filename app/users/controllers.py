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

    if None in [old_pwd, new_pwd]:
        return make_response(json.jsonify(result_en='Something Not Entered'
                                          , result_ko='입력되지 않은 값이 있습니다'
                                          , result=460), 460)

    is_done = model.update_password(current_user.id, old_pwd, new_pwd)

    if is_done == 1:
        return make_response(json.jsonify(result_en='OK'
                                          , result_ko='완료'
                                          , result=200), 200)
    elif is_done == 2:
        return make_response(json.jsonify(result_en='Password is wrong'
                                          , result_ko='잘못된 비밀번호를 입력했습니다'
                                          , result=465), 465)
    elif is_done == 0:
        return make_response(json.jsonify(result_en='Something Wrong'
                                          , result_ko='일시적인 오류로 실패했습니다'
                                          , result=461), 461)


@login_required
def change_nickname():
    nickname = request.form.get('nickname', None)

    is_done = model.update_nickname(current_user.id, nickname)

    if is_done is True:
        return make_response(json.jsonify(result_en='OK'
                                          , result_ko='완료'
                                          , result=200), 200)
    else:
        return make_response(json.jsonify(result_en='Something Wrong'
                                          , result_ko='일시적인 오류로 실패했습니다'
                                          , result=461), 461)


def change_picture():
    pass
