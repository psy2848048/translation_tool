from flask import Blueprint
import app.users.controllers as ctrl

users = Blueprint('users', __name__)

# 사용자 정보 조회
users.add_url_rule('/me', view_func=ctrl.get_user_info, methods=['GET'])

# 비밀번호 변경
users.add_url_rule('/me/pwd', view_func=ctrl.change_password, methods=['POST'])
