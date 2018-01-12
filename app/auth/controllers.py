from flask import request, make_response, json
import app.auth.models as model
from app import app

from flask_login import LoginManager, login_user, login_required, current_user, logout_user
login_manager = LoginManager()
login_manager.init_app(app)

def sign_in():
    email = request.form.get('email', None)
    password = request.form.get('password', None)

    if None in [email, password]:
        return make_response(json.jsonify(result='Something Not Entered'), 460)

    #: email&password 형식 검사
    #: email로 꺼낸 사용자의 비밀번호와 입력된 비밀번호가 일치하는지 검사한다
    #: 일치한다면 login_user에 user 정보를 넣는다

    #: 입력된 email의 사용자 찾기
    user = model.select_user_by_email(email)
    uid = user.get_id()

    if not user:
        return make_response(json.jsonify(result='User does not exist'), 401)
    else:
        #: 존재하는 사용자라면 입력된 password가 맞는지 확인
        is_ok = model.verify_password(password, uid)

        if is_ok is False:
            return make_response(json.jsonify(result="Password is wrong"), 401)
        else:
            #: 비밀번호가 일치한다면 login_user에 user 정보를 넣고, 로그인 완료!
            login_user(user, remember=True)
            return make_response(json.jsonify(result="User '{}' signed in!".format(current_user.id)), 200)

@login_manager.user_loader
def user_loader():
    user = current_user
    return user

@login_required
def sign_out():
    uid = current_user.id
    logout_user()
    return make_response(json.jsonify(result="User '%s' signed out!".format(uid)), 200)

@login_required
def print_user():
    user = current_user
    return make_response(json.jsonify(user=dict(user)), 200)
