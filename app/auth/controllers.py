from flask import request, make_response, json, url_for, session, redirect, jsonify
import app.auth.models as model
from app import app
import traceback
import requests
from pprint import pprint

from flask_login import LoginManager, login_user, login_required, logout_user, current_user
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

import google.oauth2.credentials
import google_auth_oauthlib.flow
import googleapiclient.discovery
CLIENT_SECRETS_FILE = "google_client_secret.json"
SCOPES = ['https://www.googleapis.com/auth/plus.login'
    , 'https://www.googleapis.com/auth/plus.me'
    , 'https://www.googleapis.com/auth/userinfo.profile'
    , 'https://www.googleapis.com/auth/userinfo.email']


@login_manager.user_loader
def user_loader(uid):
    user = model.select_user_info_by_email(uid)
    return user


#: 로컬
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

    #: 존재하는 사용자인지 확인하기
    user, is_ok = model.select_user_by_email(email)

    if is_ok in [1, 2]:
        return make_response(json.jsonify(result_en='This email already exists'
                                          , result_ko='이미 가입된 이메일입니다'
                                          , result=260), 260)

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
                                          , result_ko='일시적인 오류로 실패했습니다'
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
        return make_response(json.jsonify(result_en='Certification is complete!'
                                          , result_ko='인증이 완료되었습니다!'
                                          , result=200), 200)
    elif is_done is 2:
        return make_response(json.jsonify(result_en='You entered an incorrect value'
                                          , result_ko='잘못된 이메일 또는 인증코드를 입력했습니다'
                                          , result=401), 401)
    else:
        return make_response(json.jsonify(result_en='Something Wrong'
                                          , result_ko='일시적인 오류로 실패했습니다'
                                          , result=461), 461)


def local_signin():
    """
    로컬 로그인
    """
    #: 세션 비우기용
    signout()

    email = request.form.get('email', None)
    password = request.form.get('password', None)

    if None in [email, password]:
        return make_response(json.jsonify(result_en='Something Not Entered'
                                          , result_ko='입력되지 않은 값이 있습니다'
                                          , result=460), 460)

    #: 입력된 email의 사용자 찾기
    user, is_ok = model.select_user_by_email(email)

    if is_ok == 0:
        return make_response(json.jsonify(result_en='User does not exist'
                                          , result_ko='존재하지 않는 사용자입니다'
                                          , result=464), 464)
    elif is_ok == 2:
        return make_response(json.jsonify(result_en='Unauthenticated User'
                                          , result_ko='인증되지 않은 사용자입니다'
                                          , result=403), 403)
    else:
        #: 존재하는 사용자라면 입력된 password가 맞는지 확인
        is_ok = user.can_login(password)

        #: 비밀번호가 일치한다면 login_user에 user 정보를 넣고, 로그인 완료!
        if is_ok is True:
            login_user(user, remember=True)
            session['user_nickname'] = current_user.nickname

            return make_response(json.jsonify(result_en="Successfully sign-in!"
                                              , result_ko="로그인 성공!"
                                              , result=200), 200)
        else:
            return make_response(json.jsonify(result_en="Password is wrong"
                                              , result_ko='잘못된 비밀번호를 입력했습니다'
                                              , result=465), 465)


#: 페이스북
@login_required
def facebook_signin():
    email = current_user.id
    return facebook.authorize(callback=url_for('auth.facebook_authorized', email=email
                                               , next=request.args.get('next') or None
                                               , _external=True))


def facebook_authorized():
    email = request.values.get('email', None)

    try:
        resp = facebook.authorized_response()
    except:
        traceback.print_exc()
        return make_response(json.jsonify(result_en='Facebook currently works abnormally'
                                          , result_ko='페이스북의 일시적인 오류입니다'
                                          , result=466), 466)

    if resp is None:
        return make_response(jsonify(message='Access denied'
                                     , error_reason=request.args['error_reason']
                                     , error_description=request.args['error_description']))
    elif 'access_token' not in resp:
        return make_response(json.jsonify(result_en='No access token from facebook'
                                          , result_ko='페이스북이 Access Token을 보내지 않았습니다'
                                          , result=403), 403)

    #: 페이스북에서 사용자의 데이터 가져오기 - 이메일, 이름, 프로필사진
    session['facebook_token'] = (resp['access_token'], '')
    data = facebook.get('/me?fields=email,name,picture').data

    ### 이메일이 없는 경우도 있으니까 일단 이건 보류
    # if None in data:
    #     return make_response(json.jsonify(result_en='Facebook has not sent any data'
    #                                       , result_ko='페이스북에서 정보를 제대로 보내지 않았습니다'
    #                                       , result=467), 467)

    #: 존재하는 사용자인지 확인
    user = model.select_user_by_facebook_id(data.get('id'))
    if not user:
        is_done = model.update_user_social_info('facebook', email, facebook_id=data.get('id'))
        if is_done is False:
            return make_response(json.jsonify(result_en='Something Wrong'
                                              , result_ko='일시적인 오류로 실패했습니다'
                                              , result=461), 461)
        # return make_response(json.jsonify(result_en='No linked accounts. Please sign up email first'
        #                                   , result_ko='연동된 계정이 없습니다. 이메일로 먼저 회원가입을 해주세요'
        #                                   , result=401), 401)

    # login_user(user, remember=True)
    # session['user_nickname'] = current_user.nickname
    session['user_picture'] = data['picture']['data']['url']

    return make_response(json.jsonify(result_en="Connection complete"
                                      , result_ko="페이스북 연동 완료"
                                      , result=200), 200)


@facebook.tokengetter
def facebook_tokengetter(token=None):
    return session.get('facebook_token')


#: 구글
@login_required
def google_signin():
    if 'google_credentials' not in session:
        return redirect(url_for('auth.google_authorized'))

    # Load credentials from the session.
    credentials = google.oauth2.credentials.Credentials(**session['google_credentials'])

    # drive = googleapiclient.discovery.build('oauth2', 'v1', credentials=credentials)
    # files = drive.files().list().execute()

    session['google_credentials'] = google_credentials_to_dict(credentials)

    authorization_header = {"Authorization": "OAuth %s" % session['google_credentials']['token']}
    res = requests.get('https://www.googleapis.com/oauth2/v2/userinfo', headers=authorization_header)
    userinfo = json.loads(res.text)
    pprint(userinfo)

    #: 존재하는 사용자인지 확인
    user = model.select_user_by_facebook_id(userinfo['id'])
    if not user:
        is_done = model.update_user_social_info('google', userinfo['email'], google_id=userinfo['id'])
        if is_done is False:
            return make_response(json.jsonify(result_en='Something Wrong'
                                              , result_ko='일시적인 오류로 실패했습니다'
                                              , result=461), 461)

    # login_user(user, remember=True)
    # session['user_nickname'] = current_user.nickname
    session['user_picture'] = userinfo['picture']

    # Save credentials back to session in case access token was refreshed.
    # ACTION ITEM: In a production app, you likely want to save these credentials in a persistent database instead.
    session['google_credentials'] = google_credentials_to_dict(credentials)

    return make_response(json.jsonify(result_en="Connection complete"
                                      , result_ko="구글 연동 완료"
                                      , result=200), 200)


def google_authorized():
    # Create flow instance to manage the OAuth 2.0 Authorization Grant Flow steps.
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(CLIENT_SECRETS_FILE, scopes=SCOPES)

    flow.redirect_uri = url_for('auth.google_oauth2callback', _external=True)

    authorization_url, state = flow.authorization_url(
        # Enable offline access so that you can refresh an access token without
        # re-prompting the user for permission. Recommended for web server apps.
        access_type='offline',
        # Enable incremental authorization. Recommended as a best practice.
        include_granted_scopes='true')

    # Store the state so the callback can verify the auth server response.
    session['google_state'] = state

    return redirect(authorization_url)


def google_oauth2callback():
    # Specify the state when creating the flow in the callback so that it can
    # verified in the authorization server response.
    state = session['google_state']

    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(CLIENT_SECRETS_FILE, scopes=SCOPES, state=state)
    flow.redirect_uri = url_for('auth.google_oauth2callback', _external=True)

    # Use the authorization server's response to fetch the OAuth 2.0 tokens.
    authorization_response = request.url
    flow.fetch_token(authorization_response=authorization_response)

    # Store credentials in the session.
    # ACTION ITEM: In a production app, you likely want to save these credentials in a persistent database instead.
    session['google_credentials'] = google_credentials_to_dict(flow.credentials)

    return redirect(url_for('auth.google_signin'))


def google_revoke():
    if 'google_credentials' not in session:
        return ('You need to <a href="/authorize">authorize</a> before ' +
                'testing the code to revoke credentials.')

    credentials = google.oauth2.credentials.Credentials(**session['google_credentials'])

    revoke = requests.post('https://accounts.google.com/o/oauth2/revoke',
                           params={'token': credentials.token},
                           headers={'content-type': 'application/x-www-form-urlencoded'})

    status_code = getattr(revoke, 'status_code')
    if status_code == 200:
        return make_response(jsonify(result='Credentials successfully revoked.'))
    else:
        return make_response(jsonify(result='An error occurred.'))


def google_credentials_to_dict(credentials):
  return {'token': credentials.token,
          'refresh_token': credentials.refresh_token,
          'token_uri': credentials.token_uri,
          'client_id': credentials.client_id,
          'client_secret': credentials.client_secret,
          'scopes': credentials.scopes}


#: 로그아웃
def signout():
    for key in list(session.keys()):
        session.pop(key)
    logout_user()
    return make_response(json.jsonify(result_en="Successfully sign-out!"
                                      , result_ko='로그아웃 성공!'
                                      , result=200), 200)


#: (테스트용) 세션 확인
def get_session():
    return make_response(jsonify(**session), 200)
