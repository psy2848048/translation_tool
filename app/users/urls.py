from flask import Blueprint
import app.users.controllers as ctrl

users = Blueprint('users', __name__)
users.add_url_rule('/', view_func=ctrl.signup, methods=['POST'])
users.add_url_rule('/<int:user_id>', view_func=ctrl.get_user_info, methods=['GET'])
users.add_url_rule('/<int:user_id>', view_func=ctrl.modify_user_info, methods=['PUT'])
