from flask import request, make_response, json, send_file, session
from flask_login import login_required, current_user
from app import app
import app.users.models as model
import io


@login_required
def get_profile():
    return make_response(json.jsonify(current_user.profile), 200)


@login_required
def get_thumbnail():
    picture = model.select_user_thumbnail(current_user.idx)
    return send_file(picture, mimetype='image/jpeg')


@login_required
def get_thumbnail_original():
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

    is_done = model.update_picture(current_user.id, picture)

    if is_done is 1:
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


def test_picture():
    import requests
    # purl = request.values.get('picture', None)
    purl = 'https://marocat.s3.amazonaws.com/profile/20180207062149fO7f0J5a6c8Na.jpeg?AWSAccessKeyId=AKIAIPUIPGMGOME2HTNQ&amp;Signature=7paNzAJQhr2D0WRD%2B1W3sgQpk0Y%3D&amp;Expires=1517988110'
    r = requests.get(purl)

    # return io.BytesIO(r.content)
    return send_file(io.BytesIO(r.content), mimetype=r.headers['Content-Type'], as_attachment=True, attachment_filename='user_picture.jpg')


def test_s3_getobjectlink():
    import boto3
    from app import app
    S3 = boto3.client(
        's3',
        aws_access_key_id=app.config['AWS_ACCESS_KEY_ID'],
        aws_secret_access_key=app.config['AWS_SECRET_ACCESS_KEY']
        # aws_session_token=SESSION_TOKEN,
    )
    BUCKET_NAME = 'marocat'
    pname = 'profile/20180207062149fO7f0J5a6c8Na.jpeg'

    # res = S3.get_bucket_location(Bucket=BUCKET_NAME)
    # object_url = "https://s3-{0}.amazonaws.com/{1}/{2}".format(
    #     res['LocationConstraint'],
    #     BUCKET_NAME,
    #     'profile/20180207062149fO7f0J5a6c8Na.jpeg')
    # return make_response(json.jsonify(url=object_url, **res), 200)

    obj = S3.get_object(
        Bucket=BUCKET_NAME,
        Key=pname
    )
    from pprint import pprint
    pprint(obj)
    return send_file(io.BytesIO(obj['Body'].read()), mimetype='image/jpeg')
