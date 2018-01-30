from flask import Blueprint
import app.auth.controllers as ctrl

auth = Blueprint('auth', __name__)

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


# 비밀번호 복구 인증코드 이메일 보내기
auth.add_url_rule('/recoverPwd/sendCode', view_func=ctrl.send_password_recovery_email, methods=['POST'])

# 비밀번호 복구
auth.add_url_rule('/recoverPwd', view_func=ctrl.recover_password, methods=['POST'])
