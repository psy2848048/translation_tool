from flask import request, make_response, json, send_file
from flask_login import login_required, current_user
import app.users.models as model
import requests
import io

@login_required
def get_user_info():
    user_info = current_user.info

    # r = requests.get(user_info['picture_url'])
    # r = requests.get('https://lh4.googleusercontent.com/-v1oPGZT1bRw/AAAAAAAAAAI/AAAAAAAAAAc/j2WHAh6A1Cg/photo.jpg')
    # picture = io.BytesIO(r.content)
    # del user_info['picture_url']
    # del user_info['picture_s3key']

    # return make_response(json.jsonify(user_info)
    #                      , send_file(io.BytesIO(r.content), mimetype=r.headers['Content-Type'], as_attachment=False, attachment_filename='user_picture.jpg'))

    # response = make_response(json.jsonify(picture))
    # cd = 'attachment; filename={}'.format('test.png')
    # response.headers['Content-Disposition'] = cd
    # del user_info['picture_url']
    # del user_info['picture_s3key']
    # return response

    return make_response(json.jsonify(user_info), 200)


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


def test_picture():
    purl = request.values.get('picture', None)
    r = requests.get(purl)

    # return io.BytesIO(r.content)
    return send_file(io.BytesIO(r.content), mimetype=r.headers['Content-Type'], as_attachment=True, attachment_filename='user_picture')
