from flask import Blueprint
import app.auth.controllers as ctrl

auth = Blueprint('auth', __name__)

auth.add_url_rule('/local/signin', view_func=ctrl.sign_in, methods=['POST'])  # 로그인
auth.add_url_rule('/local/signout', view_func=ctrl.sign_out, methods=['GET'])  # 로그아웃
auth.add_url_rule('/check', view_func=ctrl.print_user, methods=['GET'])
