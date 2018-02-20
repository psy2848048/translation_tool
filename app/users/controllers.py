from flask import request, make_response, json, send_file, session
from flask_login import login_required, current_user
import app.users.models as model


@login_required
def get_profile():
    return make_response(json.jsonify(current_user.profile), 200)


@login_required
def get_thumbnail(picture_name):
    picture = model.select_user_thumbnail(current_user.idx)
    return send_file(picture, mimetype='image/jpeg')


@login_required
def get_thumbnail_original(picture_name):
    picture = model.select_user_thumbnail_original(current_user.idx)
    return send_file(picture, mimetype='image/jpeg')


@login_required
def change_password():
    new_pwd = request.form.get('new_pwd', None)

    if None in [new_pwd]:
        return make_response(json.jsonify(result_en='Something Not Entered'
                                          , result_ko='입력되지 않은 값이 있습니다'
                                          , result=460), 460)
    #: 비밀번호 검사
    elif len(new_pwd) < 4:
        return make_response(json.jsonify(result_en='Password must be at least 4 digits'
                                          , result_ko='비밀번호는 4자리 이상이어야 합니다.'
                                          , result=467), 467)

    is_done = model.update_password(current_user.id, new_pwd)

    if is_done == 1:
        return make_response(json.jsonify(result_en='Password changed successfully!'
                                          , result_ko='비밀번호가 변경되었습니다!'
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
    if nickname is None:
        return make_response(json.jsonify(result_en='Something Not Entered'
                                          , result_ko='입력되지 않은 값이 있습니다'
                                          , result=460), 460)

    is_done = model.update_nickname(current_user.id, nickname)

    if is_done is True:
        session['user_nickname'] = nickname
        return make_response(json.jsonify(result_en='Nickname changed successfully!'
                                          , result_ko='닉네임이 변경되었습니다!'
                                          , result=200), 200)
    else:
        return make_response(json.jsonify(result_en='Something Wrong'
                                          , result_ko='일시적인 오류로 실패했습니다'
                                          , result=461), 461)


@login_required
def change_picture():
    picture = request.files.get('picture', None)
    if picture is None:
        return make_response(json.jsonify(result_en='Something Not Entered'
                                          , result_ko='입력되지 않은 값이 있습니다'
                                          , result=460), 460)

    is_done, user_picture = model.update_picture(current_user.id, picture)

    if is_done is 1:
        session['user_picture'] = user_picture
        return make_response(json.jsonify(result_en='Picture changed successfully!'
                                          , result_ko='프로필사진이 변경되었습니다!'
                                          , result=200), 200)
    elif is_done is 2:
        return make_response(json.jsonify(result_en='Picture upload failed'
                                          , result_ko='프로필 사진 업로드에 실패했습니다'
                                          , result=468), 468)
    else:
        return make_response(json.jsonify(result_en='Something Wrong'
                                          , result_ko='일시적인 오류로 실패했습니다'
                                          , result=461), 461)


@login_required
def user_withdraw():
    is_done = model.delete_user(current_user.idx)

    if is_done is True:
        return make_response(json.jsonify(result_en='You successfully left Mycattool'
                                          , result_ko='탈퇴 완료했습니다'
                                          , result=200), 200)
    else:
        return make_response(json.jsonify(result_en='Something Wrong'
                                          , result_ko='일시적인 오류로 실패했습니다'
                                          , result=461), 461)
