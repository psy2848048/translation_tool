from flask import Blueprint
import app.auth.controllers as ctrl

auth = Blueprint('auth', __name__)
auth.add_url_rule('/', view_func=ctrl.index, methods=['GET'])
