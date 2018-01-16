from flask import Blueprint
import app.users.controllers as ctrl

users = Blueprint('users', __name__)

users.add_url_rule('/', view_func=ctrl.sign_up, methods=['POST'])  # 회원가입
users.add_url_rule('/me', view_func=ctrl.get_user_info, methods=['GET'])  # 사용자 정보 조회
users.add_url_rule('/me/pwd', view_func=ctrl.change_password, methods=['POST'])  # 사용자 정보 조회
