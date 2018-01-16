from flask import Blueprint
import app.auth.controllers as ctrl

auth = Blueprint('auth', __name__)

auth.add_url_rule('/local/signin', view_func=ctrl.sign_in, methods=['POST'])  # 로그인
auth.add_url_rule('/local/signout', view_func=ctrl.sign_out, methods=['GET'])  # 로그아웃

auth.add_url_rule('/pwRecovery/request', view_func=ctrl.send_password_recovery_email, methods=['POST'])  # 비밀번호 복구 인증코드 이메일 보내기
auth.add_url_rule('/pwRecovery', view_func=ctrl.recover_password, methods=['POST'])  # 비밀번호 복구
