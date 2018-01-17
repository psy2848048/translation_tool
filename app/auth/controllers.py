from flask import request, make_response, json
import app.auth.models as model
from app import app, common

from flask_login import LoginManager, login_user, login_required, current_user, logout_user
login_manager = LoginManager()
login_manager.init_app(app)

def sign_in():
    email = request.form.get('email', None)
    password = request.form.get('password', None)

    if None in [email, password]:
        return make_response(json.jsonify(result='Something Not Entered'), 460)

    #: 입력된 email의 사용자 찾기
    user = model.select_user_by_email(email)

    if not user:
        return make_response(json.jsonify(result='User does not exist'), 401)
    else:
        #: 존재하는 사용자라면 입력된 password가 맞는지 확인
        is_ok = user.can_login(password)

        #: 비밀번호가 일치한다면 login_user에 user 정보를 넣고, 로그인 완료!
        if is_ok is True:
            login_user(user, remember=True)
            return make_response(json.jsonify(result="User '{}' signed in!".format(user.get_id())), 200)
        else:
            return make_response(json.jsonify(result="Password is wrong"), 401)


@login_manager.user_loader
def user_loader(uid):
    user = model.select_user_by_uid(uid)
    return user


@login_required
def sign_out():
    uid = current_user.id
    print(current_user.id)
    logout_user()
    return make_response(json.jsonify(result="User '{}' signed out!".format(uid)), 200)


def send_password_recovery_email():
    email = request.form.get('email', None)

    if not email:
        return make_response(json.jsonify(result='Email Not Entered'), 460)

    #: 인증코드 만들기
    authcode, is_done, msg = model.create_auth_code(email)
    print(authcode, is_done, msg)

    if is_done is False:
        return make_response(json.jsonify(result=msg), 461)

    #: 인증코드 이메일 보내기
    # 인증코드, 비밀번호 변경할 수 있는 링크 포함해서 보내기
    title = '비밀번호 복구 인증코드입니다.'
    content = ''
    is_done = common.send_mail(email, title, content)

    if is_done is True:
        return make_response(json.jsonify(result=msg), 200)
    else:
        return make_response(json.jsonify(result='Something Wrong!'), 461)


def recover_password():
    email = request.form.get('email', None)
    authcode = request.form.get('authcode', None)
    new_pwd = request.form.get('new_pwd', None)

    if None in [email, authcode, new_pwd]:
        return make_response(json.jsonify(result='Email Not Entered'), 460)

