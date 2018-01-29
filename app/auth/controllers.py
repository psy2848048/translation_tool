from flask import request, make_response, json, url_for, session, redirect, jsonify
import app.auth.models as model
from app import app, common
from pprint import pprint
import requests

from flask_login import LoginManager, login_user, login_required, current_user, logout_user
login_manager = LoginManager()
login_manager.init_app(app)


#: 로컬 로그인
def local_signin():
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


#: 구글 로그인


#: 페이스북 로그인
from flask_oauthlib.client import OAuth
oauth = OAuth()


facebook = oauth.remote_app(
    'facebook',
    base_url='https://graph.facebook.com/',
    request_token_url=None,
    access_token_url='/oauth/access_token',
    authorize_url='https://www.facebook.com/dialog/oauth',
    consumer_key=app.config['FACEBOOK_APP_ID'],
    consumer_secret=app.config['FACEBOOK_APP_SECRET'],
    request_token_params={'scope': 'email'}
)


@facebook.tokengetter
def get_facebook_token():
    if 'facebook_oauth' in session:
        resp = session['facebook_oauth']
        return resp['oauth_token'], resp['oauth_token_secret']


def faceobook_signin():
    return facebook.authorize(callback=url_for('auth.facebook_authorized'
                                               # , next = request.args.get('next') or request.referrer or None))
                                               , _external=True))


def facebook_authorized():
    res = facebook.authorized_response()
    pprint(dict(res))
    if res is None or 'access_token' not in res:
        return make_response(json.jsonify(message="No access token from Facebook"), 403)

    session['facebook_token'] = (res['access_token'], '')
    data = facebook.get('/me?fields=email').data

    email = data.get('email')
    if email is None:
        return "Facebook currently works abnormally. Please wait a few hours."

    user = model.select_user_by_email(email)
    print(user)

    # 존재하지 않는 사용자인 경우 회원가입 페이지로 넘긴다
    if not user:
        return redirect('/static/front/user/signup.html?type=f&email={}&name={}'.format(user['email'], user['name']))

    # 이미 존재하지만 페이스북으로 가입한 적 없는 사용자에게 페이스북도 연동할지 확인하는 페이지로 넘어간다
    elif user or (user['joined_google'] is True):
        return make_response(json.jsonify(result='Already exist user'), 200)

    # 페이스북으로 이미 가입한 사용자면 그냥 로그인?
    elif user['joined_facebook'] is True:
        return make_response(json.jsonify(result='Already joined Facebook'), 200)


@login_required
def local_signout():
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

