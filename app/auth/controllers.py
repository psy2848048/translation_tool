from flask import request, make_response, json, url_for, session, redirect, jsonify
import app.auth.models as model
from app import app
from pprint import pprint

from flask_login import LoginManager, login_user, login_required, current_user, logout_user
login_manager = LoginManager()
login_manager.init_app(app)

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


def local_signup():
    """
    로컬 회원가입
    """
    name = request.form.get('nickname', None)
    email = request.form.get('email', None)
    password = request.form.get('password', None)

    if None in [email, password, name]:
        return make_response(json.jsonify(result_en='Something Not Entered'
                                          , result_ko='입력되지 않은 값이 있습니다'
                                          , result=460), 460)

    #: 사용자 DB에 저장 + 인증 이메일 보내기
    is_done = model.insert_user(name, email, password)

    if is_done is True:
        return make_response(json.jsonify(result_en='Congratulation! You successfully sign-up!'
                                          , result_ko='축하합니다! 회원가입에 성공했습니다!'
                                          , result=200), 200)
    elif is_done is 2:
        return make_response(json.jsonify(result_en='This email already exists'
                                          , result_ko='이미 가입된 이메일입니다'
                                          , result=260), 260)
    else:
        return make_response(json.jsonify(result_en='Something Wrong'
                                          , result_ko='서버 작업 중에 오류 발생'
                                          , result=461), 461)


def cert_local_signup():
    """
    로컬 회원가입 인증
    """
    email = request.values.get('email', None)
    cert_token = request.values.get('cert_token', None)

    if None in [email, cert_token]:
        return make_response(json.jsonify(result='Something Not Entered'), 460)

    is_done = model.update_user_local_info(email, cert_token)

    if is_done is True:
        return make_response(json.jsonify(result_en='OK'
                                          , result_ko='성공'
                                          , result=200), 200)
    elif is_done is 2:
        return make_response(json.jsonify(result_en='You entered an incorrect value'
                                          , result_ko='잘못된 이메일 또는 인증코드를 입력했습니다'
                                          , result=401), 401)
    else:
        return make_response(json.jsonify(result_en='Something Wrong'
                                          , result_ko='서버 작업 중에 오류 발생'
                                          , result=461), 461)


def local_signin():
    """
    로컬 로그인
    """
    email = request.form.get('email', None)
    password = request.form.get('password', None)

    if None in [email, password]:
        return make_response(json.jsonify(result_en='Something Not Entered'
                                          , result_ko='입력되지 않은 값이 있습니다'
                                          , result=460), 460)

    #: 입력된 email의 사용자 찾기
    user, cert_local = model.select_user_by_email(email)

    if cert_local == 0:
        return make_response(json.jsonify(result_en='User does not exist'
                                          , result_ko='존재하지 않는 사용자입니다'
                                          , result=401), 401)
    elif cert_local == 2:
        return make_response(json.jsonify(result_en='Unauthenticated User'
                                          , result_ko='인증되지 않은 사용자입니다'
                                          , result=403), 403)
    else:
        #: 존재하는 사용자라면 입력된 password가 맞는지 확인
        is_ok = user.can_login(password)

        #: 비밀번호가 일치한다면 login_user에 user 정보를 넣고, 로그인 완료!
        if is_ok is True:
            login_user(user, remember=True)
            pprint(session)

            return make_response(json.jsonify(result_en="Successfully sign-in!"
                                          , result_ko="로그인 성공!"
                                          , result=200), 200)
        else:
            return make_response(json.jsonify(result_en="Password is wrong"
                                          , result_ko='잘못된 비밀번호를 입력했습니다'
                                          , result=401), 401)


@login_manager.user_loader
def user_loader(uid):
    user = model.select_user_info_by_email(uid)
    return user


def facebook_signin():
    return facebook.authorize(callback=url_for('auth.facebook_authorized'
                                               , _external=True
                                               # , next=request.args.get('next') or request.referrer or None
                                               )
                              )


def facebook_authorized():
    resp = facebook.authorized_response()
    pprint(resp)

    if resp is None:
        return 'Access denied: reason=%s error=%s' % (
            request.args['error_reason'],
            request.args['error_description']
        )

    # if resp is None or 'access_token' not in resp:
    #     return make_response(json.jsonify(message="No access token from facebook"), 403)

    session['facebook_token'] = (resp['access_token'], '')
    user_data = facebook.get('/me?fields=email,name,picture').data
    pprint(user_data)

    email = user_data.get('email')
    if email is None:
        return make_response(json.jsonify(message="Facebook currently works abnormally. Please wait a few hours."), 403)

    # user_id = model.select_user_by_email(email)
    # if user_id == -1:
    #     return redirect('/evaluation2/joinus?email={}'.format(email))
    #
    # else:
    #     data = model.getUserInfo(email)
    #     session['logged_in'] = True
    #     session['email'] = email
    #     for key, value in data.items():
    #         session[key] = value
    #
    #     return redirect('/evaluation2')
    return make_response(json.jsonify(message='Done!'), 200)


@facebook.tokengetter
def facebook_tokengetter(token=None):
    return session.get('facebook_token')
    # if 'facebook_oauth' in session:
    #     resp = session['facebook_oauth']
    #     return resp['oauth_token'], resp['oauth_token_secret']


@login_required
def local_signout():
    logout_user()
    return make_response(json.jsonify(result_en="Successfully sign-out!"
                                      , result_ko='로그아웃 성공!'
                                      , result=200), 200)


def get_session():
    return make_response(jsonify(session=dict(session)), 200)