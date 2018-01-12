from flask import Blueprint
import app.users.controllers as ctrl

users = Blueprint('users', __name__)

users.add_url_rule('/', view_func=ctrl.sign_up, methods=['POST'])   # 회원가입
