from flask import Blueprint
import app.users.controllers as ctrl

users = Blueprint('users', __name__)

# 사용자 정보 조회
users.add_url_rule('/me', view_func=ctrl.get_user_profile, methods=['GET'])

users.add_url_rule('/me/pwd', view_func=ctrl.change_password, methods=['PUT'])
users.add_url_rule('/me/nickname', view_func=ctrl.change_nickname, methods=['PUT'])
users.add_url_rule('/me/picture', view_func=ctrl.change_picture, methods=['PUT'])


#: 테스트용
users.add_url_rule('/me/bye', view_func=ctrl.user_withdraw, methods=['DELETE'])
users.add_url_rule('/test', view_func=ctrl.test_picture, methods=['GET'])
