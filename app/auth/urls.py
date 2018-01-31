from flask import Blueprint
import app.auth.controllers as ctrl

auth = Blueprint('auth', __name__)

# 로컬 회원가입
auth.add_url_rule('/local/signup', view_func=ctrl.local_signup, methods=['POST'])

# 로컬 회원가입 인증
auth.add_url_rule('/local/cert', view_func=ctrl.cert_local_signup, methods=['POST'])

# 로컬 로그인
auth.add_url_rule('/local/signin', view_func=ctrl.local_signin, methods=['POST'])


# 구글 로그인
# auth.add_url_rule('/google/signin', view_func=ctrl.google_signin, methods=['GET'])
# auth.add_url_rule('/google/oauth2callback', view_func=ctrl.google_signin, methods=['GET'])

# 페이스북 로그인
auth.add_url_rule('/facebook/signin', view_func=ctrl.facebook_signin, methods=['GET'])
auth.add_url_rule('/facebook/callback', view_func=ctrl.facebook_callback, methods=['GET'])
auth.add_url_rule('/facebook/tokengetter', view_func=ctrl.facebook_tokengetter, methods=['GET'])

# 로그아웃
auth.add_url_rule('/local/signout', view_func=ctrl.local_signout, methods=['GET'])
