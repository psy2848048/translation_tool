from flask import Blueprint
import app.steem.controllers as ctrl

steem = Blueprint('steem', __name__)

steem.add_url_rule('/trans/request', view_func=ctrl.request_trans, methods=['POST'])
steem.add_url_rule('/trans/post', view_func=ctrl.post_export_and_save, methods=['POST'])
